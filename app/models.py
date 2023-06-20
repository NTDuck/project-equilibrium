
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from . import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, index=True)
    username = db.Column(db.String(32), unique=True, index=True)
    password_hash = db.Column(db.String(512))

    todolist = db.relationship("Todolist", backref="user", lazy=True)
    timer_session_count = db.relationship("TimerSessionCount", backref="user", lazy=True)
    chatbot_message = db.relationship("ChatbotMessage", backref="user", lazy=True)

    @property
    def password(self):
        raise AttributeError
    
    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password=password)
    
    def verify_password(self, password: str):
        return check_password_hash(self.password_hash, password=password)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128), index=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class TimerSessionCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    session_count = db.Column(db.SmallInteger, nullable=False, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class ChatbotMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(512), nullable=False)
    type = db.Column(db.String(8), nullable=False, default="server")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)