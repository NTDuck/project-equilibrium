
from flask import Blueprint
api = Blueprint("api", __name__)

from . import audio, timer, data, todolist, chatbot