
from . import db


class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128), index=True, nullable=False)


class TimerSessionCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    session_count = db.Column(db.SmallInteger, nullable=False, default=0)