
import os
import json
from datetime import date
from config import Config
from .models import Todolist, TimerSessionCount


class AbstractDbHandler:
    def __init__(self, request, db):
        self.request = request
        self.db = db
    
    def commit_session(self):
        self.db.session.commit()
        self.db.session.close()


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
        self.db.session.commit()   

    def handle_db_update(self, EditRow: TimerSessionCount):
        EditRow.session_count += 1
        self.db.session.commit()

    def delete_table(self):
        TimerSessionCount.query.delete()
        self.db.session.commit()

    def handle_db_multiple_insert(self, insert_array):
        if not self.handle_db_read():
            for [date, session_count] in insert_array:
                item = TimerSessionCount(date=date, session_count=session_count)
                self.db.session.add(item)
            self.db.session.commit()


def is_file_allowed(filename, allowed_file_exts) -> bool:
    filetype = os.path.splitext(filename)[-1]
    return filetype in allowed_file_exts


def validate_json_data(file) -> dict | bool:
    # current structure: data = {
    #     "todolist": list[str],
    #     "timer-session-count": list[list[date_string, int]],
    # }

    # check if file is empty\
    # warning: event never received, error might occur in production
    if file.filename == "":
        return False

    if not is_file_allowed(file.filename, Config.ALLOWED_FILE_EXTENSIONS_USER_DATA):
        return False

    file_content = file.read()
    json_data = json.loads(file_content)
    
    # check if data is readable dict
    if not isinstance(json_data, dict):
        return False
    
    # check if data contains only valid keys
    if json_data.keys() != {"todolist", "timer-session-count"}:
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
        for [date_string, session_count] in timer_session_counts:
            if any([
                not isinstance(session_count, int),
                session_count < 0,
            ]):
                return False
            date.fromisoformat(date_string)   # check if date_string is stored in valid iso format
    except ValueError:
        return False
    
    return json_data