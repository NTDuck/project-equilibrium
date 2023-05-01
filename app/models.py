
from flask_login import UserMixin
from werkzeug.security import (
    check_password_hash, generate_password_hash, 
)

from . import (
    db, login_manager, 
)   # potential bug: config.Config not initialized when called


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    rel_pomodoro_config = db.relationship("PomodoroConfig", backref="users", uselist=False)   # one-to-one rel with pomodoro_config

    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

    @property
    def password(self):
        raise AttributeError("<password> is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
    

class PomodoroConfig(db.Model):
    __tablename__ = "pomodoro_config"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    work_minutes = db.Column(db.Integer, index=True, nullable=False, default=45)
    short_break_minutes = db.Column(db.Integer, index=True, nullable=False, default=5)
    long_break_minutes = db.Column(db.Integer, index=True, nullable=False, default=25)
    pomodoros_until_long_break = db.Column(db.Integer, index=True, nullable=False, default=4)

    def __repr__(self):
        return "pomodoro_config"
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))