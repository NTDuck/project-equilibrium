
import os
from .models import Todolist


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
            insert_row = Todolist(value=insert_value)
            self.db.session.add(insert_row)
            self.commit_session()

    def handle_db_update(self, prev_flag, new_flag):
        prev_value = self.request.form.get(prev_flag)
        new_value = self.request.form.get(new_flag)
        edit_row = Todolist.query.filter_by(value=prev_value).first()
        edit_row.value = new_value
        self.commit_session()

    def handle_db_delete(self, delete_flag):
        delete_value = self.request.form.get(delete_flag)
        delete_row = Todolist.query.filter_by(value=delete_value).first()
        self.db.session.delete(delete_row)
        self.commit_session()

    # custom commands

    # delete all todolist items
    def delete_table(self):
        Todolist.query.delete()
        self.commit_session()

    # insert all default items
    def handle_db_multiple_insert(self, insert_array):
        for value in insert_array:
            item = Todolist(value=value)
            self.db.session.add(item)
        self.commit_session()


class TimerSessionCountDbHandler(AbstractDbHandler):
    def __init__(self, request, db):
        super().__init__(request, db)


def is_file_allowed(filename, allowed_file_exts):
    filetype = os.path.splitext(filename)[-1]
    return filetype in allowed_file_exts