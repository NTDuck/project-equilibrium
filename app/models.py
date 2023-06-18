
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from . import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True)
    username = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))

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



"""
1. repurpose models.py:
- new user table
- method: CREATE, READ, UPDATE (attr), DELETE
- each user has an (not necessarily unique) instance of model subclasses
- update each model subclass for ref to user
2. update entire system based on user state
- logged in: required for db update; 
- not logged in: save data somewhere request-lifespan; session perhaps. should look into g obj
- logged in: save data as normal, now with additional info: user
3. store user to sessions? kinda make the current instance of user available for CRUD operations on model tables
P/S: update security features
"""