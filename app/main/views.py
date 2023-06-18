
from flask import render_template, request
from flask_login import current_user, login_required

from . import main
from .. import db
from ..utils import TodolistDbHandler, TimerSessionCountDbHandler, ChatbotMessageDbHandler, handle_timer_data


todolistDbHandler = TodolistDbHandler(request, db)
timerSessionCountDbHandler = TimerSessionCountDbHandler(request, db)
chatbotMessageDbHandler = ChatbotMessageDbHandler(request, db)


@main.route("/")
def index():
    if current_user.is_authenticated:
        todolistItems = todolistDbHandler.read()
        chatbotMessages = chatbotMessageDbHandler.read()
    else:
        # should implement some example messages
        todolistItems = []
        chatbotMessages = []
    return render_template("index.html", todolistItems=todolistItems, chatbotMessages=chatbotMessages)


# should be universal regardless of user login state
@main.route("/about")
def about():
    return render_template("views/about.html")


@main.route("/stats")
@login_required
def stats():
    raw_timer_data = timerSessionCountDbHandler.read()
    timer_data, max_session_count = handle_timer_data(raw_timer_data)
    return render_template("views/stats.html", timer_data=timer_data, max_session_count=max_session_count)


@main.route("/settings")
@login_required
def settings():
    return render_template("views/settings.html")