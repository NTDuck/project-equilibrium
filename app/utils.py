
import os
from random import random
import json
from datetime import date
from transformers import pipeline
from config import Config
from .models import Todolist, TimerSessionCount, ChatbotMessage


class AbstractDbHandler:
    def __init__(self, request, db):
        self.request = request
        self.db = db
    
    def commit_session(self):
        self.db.session.commit()


class TodolistDbHandler(AbstractDbHandler):
    def __init__(self, request, db):
        self.custom_commands = {
            "rm": self.delete_table,
        }
        super().__init__(request, db)

    # normal operations

    def handle_db_read(self):
        return Todolist.query.all()

    def handle_db_insert(self, insert_flag, command_flag="$"):
        def is_custom_command(s: str) -> bool:
            return all([
                s.startswith(command_flag),
                s.lstrip(f" {command_flag}").lower() in self.custom_commands.keys(),
            ])
        def validate(s: str) -> bool:
            return all([
                not s.isspace(),
                0 < len(s) < 128,
            ])
        
        insert_value = self.request.form.get(insert_flag).strip()
        if is_custom_command(insert_value):
            custom_command = self.custom_commands[insert_value.strip(f" {command_flag}").lower()]
            custom_command()
        elif validate(insert_value):
            InsertRow = Todolist(value=insert_value)
            self.db.session.add(InsertRow)
            self.commit_session()

    def handle_db_update(self, prev_flag, new_flag):
        prev_value = self.request.form.get(prev_flag)
        new_value = self.request.form.get(new_flag)
        EditRow = Todolist.query.filter_by(value=prev_value).first()
        EditRow.value = new_value
        self.commit_session()

    def handle_db_delete(self, delete_flag):
        delete_value = self.request.form.get(delete_flag)
        DeleteRow = Todolist.query.filter_by(value=delete_value).first()
        self.db.session.delete(DeleteRow)
        self.commit_session()

    # custom commands

    # delete all todolist items
    def delete_table(self):
        Todolist.query.delete()
        self.commit_session()

    # insert all default items
    def handle_db_multiple_insert(self, insert_array):
        if not self.handle_db_read():
            for value in insert_array:
                item = Todolist(value=value)
                self.db.session.add(item)
            self.commit_session()


class TimerSessionCountDbHandler(AbstractDbHandler):
    def __init__(self, request, db):
        super().__init__(request, db)

    def handle_db_read(self):
        return TimerSessionCount.query.all()
    
    # closing session yeilds unknown error: https://sqlalche.me/e/20/bhk3
    def handle_db_insert(self):
        InsertRow = TimerSessionCount(date=date.today(), session_count=1)
        self.db.session.add(InsertRow)
        self.commit_session() 

    def handle_db_update(self, EditRow: TimerSessionCount):
        EditRow.session_count += 1
        self.commit_session()

    def delete_table(self):
        TimerSessionCount.query.delete()
        self.commit_session()

    def handle_db_multiple_insert(self, insert_array):
        if not self.handle_db_read():
            for [date, session_count] in insert_array:
                item = TimerSessionCount(date=date, session_count=session_count)
                self.db.session.add(item)
        self.commit_session()


class ChatbotMessageDbHandler(AbstractDbHandler):
    def __init__(self, request, db):
        super().__init__(request, db)

    def handle_db_read(self):
        return ChatbotMessage.query.all()

    # only handle db insertion, logic handled elsewhere
    def handle_db_insert(self, insert_value, insert_type):
        InsertRow = ChatbotMessage(value=insert_value, type=insert_type)
        self.db.session.add(InsertRow)
        self.commit_session()

    def handle_db_update(self, prev_flag, new_flag):   # used on user msg
        # edit value of specified message
        prev_value = self.request.form.get(prev_flag)
        new_value = self.request.form.get(new_flag)
        EditRow = ChatbotMessage.query.filter_by(value=prev_value).first()
        EditRow.value = new_value
        self.commit_session()

        # delete all messages after
        ChatbotMessage.query.filter(ChatbotMessage.id > EditRow.id).delete()

        # generate new server message
        server_message = text_generation(new_value)
        self.handle_db_insert(server_message, "server")

    def handle_db_delete(self, delete_flag):
        # select last msg with specified content & delete all message after
        delete_value = self.request.form.get(delete_flag)
        DeleteRowOrigin = ChatbotMessage.query.filter_by(value=delete_value).first()
        # warning: identical values get deleted altogether
        ChatbotMessage.query.filter(ChatbotMessage.id >= DeleteRowOrigin.id).delete()
        self.commit_session()

    def server_msg_reload(self, reload_flag):   # used on server msg
        reload_value = self.request.form.get(reload_flag)
        ReloadRow = ChatbotMessage.query.filter_by(value=reload_value).first()
        ChatbotMessage.query.filter(ChatbotMessage.id >= ReloadRow.id).delete()

        # generate new server message based on content of last user msg
        last_user_msg_id = ReloadRow.id - 1
        last_user_msg_value = ChatbotMessage.query.filter_by(id=last_user_msg_id).first().value

        server_message = text_generation(last_user_msg_value)
        self.handle_db_insert(server_message, "server")

    def delete_table(self):
        ChatbotMessage.query.delete()
        self.db.session.commit()

    def handle_db_multiple_insert(self, insert_array):
        if not self.handle_db_read():
            for [value, type] in insert_array:
                item = ChatbotMessage(value=value, type=type)
                self.db.session.add(item)
            self.db.session.commit()


def is_file_allowed(filename, allowed_file_exts) -> bool:
    filetype = os.path.splitext(filename)[-1]
    return filetype in allowed_file_exts


def validate_json_data(file) -> dict | bool:
    # check if file is empty\
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
    try:
        for value in todolists:
            if any([
                not isinstance(value, str),
                len(value) >= 128,
                value.isspace(),   # check if value contains only whitespace
            ]):
                return False
            value.encode("utf-8")   # check if value contains only valid utf-8 characters
    except UnicodeEncodeError:
        return False
    
    timer_session_counts = json_data["timer-session-count"]
    try:
        # check if data contains identical date values
        date_strings = [item[0] for item in timer_session_counts]
        if len(date_strings) != len(set(date_strings)):
            return False
        for [date_string, session_count] in timer_session_counts:
            if any([
                not isinstance(session_count, int),
                session_count < 0,
            ]):
                return False
            date.fromisoformat(date_string)   # check if date_string is stored in valid iso format
    except ValueError:
        return False

    chatbot_messages = json_data["chatbot-messages"]
    try:
        values = [item[0] for item in chatbot_messages]
        types = [item[1] for item in chatbot_messages]
        for value in values:
            if any([
                not isinstance(value, str),
                len(value) >= 512,
                value.isspace(),   # check if value contains only whitespace
            ]):
                return False
            value.encode("utf-8")   # check if value contains only valid utf-8 characters
        if any([
            # check if types follows pattern ["user", "server"]
            all([
                list(set(types)) != ["user", "server"],
                types == [],
            ]),
            types != ["user", "server"] * (len(types) // 2)
        ]):
            return False
    except UnicodeEncodeError:
        return False    
    
    return json_data


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
    # return f"some fucking idiot literally said {input_text.lower()}, {random()}"