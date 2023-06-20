
import os
import re
from datetime import date

from flask import json
from flask_login import current_user
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError
from transformers import pipeline

from config import Config
from .models import User, Todolist, TimerSessionCount, ChatbotMessage


class BaseDbHandler:
    # CRUD opeartions only on current user
    def __init__(self, request, db, table):
        self.request = request
        self.db = db
        self.table = table

    def validate(self, value: str, unique_attr="value", min_str_length=Config.USER_INPUT_MIN_STRING_LENGTH, max_str_length=Config.USER_INPUT_MAX_STRING_LENGTH) -> bool:
        return all([
            min_str_length < len(value) < max_str_length,
            not value.isspace(),
            self.table.query.filter_by(**{unique_attr: value}).first() is None,
        ])
    
    def commit_session(self):
        self.db.session.commit()

    def create(self, **attrs):
        item = self.table(user=current_user, **attrs)
        self.db.session.add(item)

    def create_all(self, insert_array: list[dict[str, str]]):
        if not self.read():
            for attrs in insert_array:
                item = self.table(user=current_user, **attrs)
                self.db.session.add(item)

    def read(self) -> list:
        # pascal case to snake case
        # warning: create multiple instances of string, should be optimized
        def convert_pascal_to_snake(ClassName: type) -> str:
            s = ClassName.__name__
            for i in s:
                if i.isupper():
                    s = s.replace(i, f"_{i.lower()}")
            return s.strip("_")
        return getattr(current_user, convert_pascal_to_snake(self.table))

    def edit(self, prev_value, new_value, attr):
        item = self.table.query.filter_by(user=current_user, **{attr: prev_value}).first()
        setattr(item, attr, new_value)
    
    # should be unique to User table
    def delete_all(self):
        self.table.query.filter_by(user=current_user).delete()


class UserDbHandler(BaseDbHandler):
    def __init__(self, request, db):
        super().__init__(request, db, User)

    def validate_email(self, email: str) -> str | None:
        email = email.strip()
        if not self.validate(email, unique_attr="email", max_str_length=256):
            return None
        try:
            validated_email = validate_email(email, check_deliverability=True)
            return validated_email.normalized
        except EmailNotValidError or EmailSyntaxError:
            return None
        
    def validate_username(self, username: str) -> str | None:
        username = username.lower().strip()
        return username if all([
            re.match(pattern=Config.USER_USERNAME_REGEX_PATTERN, string=username) is not None,
            self.table.query.filter_by(username=username).first() is None,
        ]) else None
        
    def validate_password(self, password: str) -> str | None:
        password = password.strip()
        return password if re.match(pattern=Config.USER_PASSWORD_REGEX_PATTERN, string=password) is not None else None

    def create(self, **attrs):
        item = self.table(**attrs)
        self.db.session.add(item)

    def read(self):
        return self.table.query.all()

    # why does this exist lmao
    def delete_all(self):
        return self.table.query.delete()


class TodolistDbHandler(BaseDbHandler):
    def __init__(self, request, db):
        super().__init__(request, db, Todolist)

    def delete(self, value):
        item = self.table.query.filter_by(value=value).first()
        self.db.session.delete(item)


class TimerSessionCountDbHandler(BaseDbHandler):
    def __init__(self, request, db):
        super().__init__(request, db, TimerSessionCount)

    def edit(self, item: TimerSessionCount):
        item.session_count += 1


class ChatbotMessageDbHandler(BaseDbHandler):
    def __init__(self, request, db):
        super().__init__(request, db, ChatbotMessage)

    def delete(self, value, ignore_items_from_self=0):
        # select last msg with specified content & delete all message after
        item = self.table.query.filter_by(value=value).first()
        # warning: identical values get deleted altogether
        self.table.query.filter(self.table.id >= item.id + ignore_items_from_self).delete()

    def edit_server_msg(self, value) -> str:
        item = self.table.query.filter_by(value=value).first()
        self.table.query.filter(self.table.id >= item.id).delete()

        # generate new server message based on content of last user msg
        last_user_msg_id = getattr(item, "id") - 1
        last_user_msg_value = getattr(self.table.query.filter_by(id=last_user_msg_id).first(), "value")

        return last_user_msg_value


def is_file_allowed(filename, allowed_file_exts) -> bool:
    filetype = os.path.splitext(filename)[-1]
    return filetype in allowed_file_exts


def validate_json_data(file) -> dict | None:
    # check if file is empty
    # warning: event never received, error might occur in production
    if file.filename == "":
        return None

    if not is_file_allowed(file.filename, Config.USER_DATA_ALLOWED_FILE_EXTENSIONS):
        return None

    file_content = file.read()
    json_data = json.loads(file_content)
    
    # check if data is readable dict
    if not isinstance(json_data, dict):
        return None
    
    # check if data contains only valid keys
    if json_data.keys() != {"todolist", "timer-session-count", "chatbot-messages"}:
        return None
    
    # check if data.todolist contains only valid values
    todolists = json_data["todolist"]
    if len(todolists) != len(set(todolists)):
        return None
    for value in todolists:
        if any([
            not isinstance(value, str),
            len(value) >= 128,
            value.isspace(),   # check if value contains only whitespace
        ]):
            return None
    
    timer_session_counts = json_data["timer-session-count"]
    date_strings = [item[0] for item in timer_session_counts]
    session_counts = [item[1] for item in timer_session_counts]   # can contain identical values

    if len(date_strings) != len(set(date_strings)):
        return None
    for session_count in session_counts:
        if any([
            not isinstance(session_count, int),
            session_count < 0,
        ]):
            return None
    try:
        for date_string in date_strings:
            date.fromisoformat(date_string)   # check if date_string is stored in valid iso format
    except ValueError:   # raised if date_string is not in valid iso format
        return None

    chatbot_messages = json_data["chatbot-messages"]
    values = [item[0] for item in chatbot_messages]
    types = [item[1] for item in chatbot_messages]

    if len(values) != len(set(values)):
        return None
    for value in values:
        if any([
            not isinstance(value, str),
            len(value) >= 512,
            value.isspace(),   # check if value contains only whitespace
        ]):
            return None
    if any([
        # check if types follows pattern ["user", "server"]
        all([
            list(set(types)) != ["user", "server"],
            not types,   # types == []
        ]),
        types != ["user", "server"] * (len(types) // 2)
    ]):
        return None
    
    return json_data   # upon validation


def handle_timer_data(data: list[TimerSessionCount]):
    item_session_counts = [item.session_count for item in data]
    timer_data = [[item.date.strftime("%b"), item.date.strftime("%d"), item.session_count] for item in data]
    return timer_data, max(item_session_counts)


# warning: should run on multiple threads
def text_generation(input_text: str) -> str:
    generator = pipeline("text-generation", model=Config.HUGGINGFACE_MODEL)
    res = generator(
        input_text,
        min_length=Config.HUGGINGFACE_MODEL_MIN_LENGTH,
        max_length=Config.HUGGINGFACE_MODEL_MAX_LENGTH,
    )
    return res[0].get("generated_text").strip().replace("\n", "")