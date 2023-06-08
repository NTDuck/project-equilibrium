
import os
import json
from datetime import date
from transformers import pipeline
from config import Config
from .models import Todolist, TimerSessionCount, ChatbotMessage


class BaseDbHandler:
    def __init__(self, request, db, modelClass):
        self.request = request
        self.db = db
        self.modelClass = modelClass

    def validate(self, value: str, min_str_length=Config.USER_INPUT_MIN_STRING_LENGTH, max_str_length=Config.USER_INPUT_MAX_STRING_LENGTH) -> bool:
        return all([
            min_str_length < len(value) < max_str_length,
            not value.isspace(),
            value not in [getattr(item, "value") for item in self.read()],
        ])
    
    def commit_session(self):
        self.db.session.commit()

    def create(self, **attrs):
        item = self.modelClass(**attrs)
        self.db.session.add(item)

    def create_all(self, insert_array: list[dict[str, str]]):
        if not self.read():
            for attrs in insert_array:
                item = self.modelClass(**attrs)
                self.db.session.add(item)
            self.commit_session()

    def read(self) -> list:
        return self.modelClass.query.all()

    def edit(self, prev_value, new_value, attr):
        item = self.modelClass.query.filter_by(**{attr: prev_value}).first()
        setattr(item, attr, new_value)
    
    def delete_all(self):
        self.modelClass.query.delete()
        self.commit_session()


class TodolistDbHandler(BaseDbHandler):
    def __init__(self, request, db):
        super().__init__(request, db, Todolist)

    def delete(self, value):
        item = self.modelClass.query.filter_by(value=value).first()
        self.db.session.delete(item)


class TimerSessionCountDbHandler(BaseDbHandler):
    def __init__(self, request, db):
        super().__init__(request, db, TimerSessionCount)

    def edit(self, item: TimerSessionCount):
        item.session_count += 1


class ChatbotMessageDbHandler(BaseDbHandler):
    def __init__(self, request, db):
        super().__init__(request, db, ChatbotMessage)

    def edit_user_msg(self, prev_value, new_value):
        # edit value of specified message
        item = self.modelClass.query.filter_by(value=prev_value).first()
        setattr(item, "value", new_value)

        # delete all messages after
        self.modelClass.query.filter(self.modelClass.id > item.id).delete()

        # generate new server message
        server_message = text_generation(new_value)
        self.create(value=server_message, type="server")

    def delete(self, value):
        # select last msg with specified content & delete all message after
        item = self.modelClass.query.filter_by(value=value).first()
        # warning: identical values get deleted altogether
        self.modelClass.query.filter(self.modelClass.id >= item.id).delete()

    def edit_server_msg(self, value):
        item = self.modelClass.query.filter_by(value=value).first()
        self.modelClass.query.filter(self.modelClass.id >= item.id).delete()

        # generate new server message based on content of last user msg
        last_user_msg_id = item.id - 1
        last_user_msg_value = getattr(self.modelClass.query.filter_by(id=last_user_msg_id).first(), "value")

        server_message = text_generation(last_user_msg_value)
        self.create(value=server_message, type="server")


def is_file_allowed(filename, allowed_file_exts) -> bool:
    filetype = os.path.splitext(filename)[-1]
    return filetype in allowed_file_exts


def validate_json_data(file) -> dict | bool:
    # check if file is empty
    # warning: event never received, error might occur in production
    if file.filename == "":
        return False

    if not is_file_allowed(file.filename, Config.USER_DATA_ALLOWED_FILE_EXTENSIONS):
        return False

    file_content = file.read()
    json_data = json.loads(file_content)
    
    # check if data is readable dict
    if not isinstance(json_data, dict):
        return False
    
    # check if data contains only valid keys
    if json_data.keys() != {"todolist", "timer-session-count", "chatbot-messages"}:
        return False
    
    # check if data.todolist contains only valid values
    todolists = json_data["todolist"]
    if len(todolists) != len(set(todolists)):
        return False
    for value in todolists:
        if any([
            not isinstance(value, str),
            len(value) >= 128,
            value.isspace(),   # check if value contains only whitespace
        ]):
            return False
    
    timer_session_counts = json_data["timer-session-count"]
    date_strings = [item[0] for item in timer_session_counts]
    session_counts = [item[1] for item in timer_session_counts]   # can contain identical values

    if len(date_strings) != len(set(date_strings)):
        return False
    for session_count in session_counts:
        if any([
            not isinstance(session_count, int),
            session_count < 0,
        ]):
            return False
    try:
        for date_string in date_strings:
            date.fromisoformat(date_string)   # check if date_string is stored in valid iso format
    except ValueError:   # raised if date_string is not in valid iso format
        return False

    chatbot_messages = json_data["chatbot-messages"]
    values = [item[0] for item in chatbot_messages]
    types = [item[1] for item in chatbot_messages]

    if len(values) != len(set(values)):
        return False
    for value in values:
        if any([
            not isinstance(value, str),
            len(value) >= 512,
            value.isspace(),   # check if value contains only whitespace
        ]):
            return False
    if any([
        # check if types follows pattern ["user", "server"]
        all([
            list(set(types)) != ["user", "server"],
            not types,   # types == []
        ]),
        types != ["user", "server"] * (len(types) // 2)
    ]):
        return False
    
    return json_data   # upon validation


def handle_timer_data(data: list[TimerSessionCount]):
    item_session_counts = [item.session_count for item in data]
    timer_data = [[item.date.strftime("%b"), item.date.strftime("%d"), item.session_count] for item in data]
    return timer_data, max(item_session_counts)


def text_generation(input_text: str) -> str:
    generator = pipeline("text-generation", model=Config.HUGGINGFACE_MODEL)
    res = generator(
        input_text,
        min_length=Config.HUGGINGFACE_MODEL_MIN_LENGTH,
        max_length=Config.HUGGINGFACE_MODEL_MAX_LENGTH,
    )
    return res[0].get("generated_text").strip().replace("\n", "")