
from . import db


class TodolistItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128), unique=True)