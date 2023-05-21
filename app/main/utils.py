

class DbOperationHandler:

    def __init__(self, request, db, column, default_values=[]):
        self.request = request
        self.db = db
        self.column = column
        self.default_values = default_values
        self.custom_commands = {
            "rm": self.delete_column,
            "default": self.insert_default_list,
        }

    def commit_session(self):
        self.db.session.commit()
        self.db.session.close()

    # normal operations

    def handle_db_insert(self, insert_flag):
        def is_custom_command(s: str) -> bool:
            return all([
                s.startswith("$"),
                s.lstrip(" $").lower() in self.custom_commands.keys(),
            ])
        def validate(s: str) -> bool:
            return all([
                not s.isspace(),
                0 < len(s) < 128,
            ])
        
        insert_value = self.request.form.get(insert_flag).strip()
        if is_custom_command(insert_value):
            custom_command = self.custom_commands[insert_value.strip("$ ").lower()]
            custom_command()
        elif validate(insert_value):
            insert_row = self.column(value=insert_value)
            self.db.session.add(insert_row)
            self.commit_session()

    def handle_db_update(self, prev_flag, new_flag):
        prev_value = self.request.form.get(prev_flag)
        new_value = self.request.form.get(new_flag)
        edit_row = self.column.query.filter_by(value=prev_value).first()
        edit_row.value = new_value
        self.commit_session()

    def handle_db_delete(self, delete_flag):
        delete_value = self.request.form.get(delete_flag)
        delete_row = self.column.query.filter_by(value=delete_value).first()
        self.db.session.delete(delete_row)
        self.commit_session()

    # custom commands

    # delete all todolist items
    def delete_column(self):
        self.column.query.delete()
        self.commit_session()

    # insert all default items
    def insert_default_list(self):
        for value in self.default_values:
            DefaultTodolistItem = self.column(value=value)
            self.db.session.add(DefaultTodolistItem)
        self.commit_session()