
from flask import render_template, request
from . import main
from .. import db
from ..utils import TodolistDbHandler, TimerSessionCountDbHandler, ChatbotMessageDbHandler, handle_timer_data


todolistDbHandler = TodolistDbHandler(request, db)
timerSessionCountDbHandler = TimerSessionCountDbHandler(request, db)
chatbotMessageDbHandler = ChatbotMessageDbHandler(request, db)


@main.route("/")
def index():
    return render_template("index.html", todolistItems=todolistDbHandler.read(), chatbotMessages=chatbotMessageDbHandler.read())


@main.route("/about")
def about():
    return render_template("views/about.html")


@main.route("/stats")
def stats():
    raw_timer_data = timerSessionCountDbHandler.read()
    timer_data, max_session_count = handle_timer_data(raw_timer_data)
    return render_template("views/stats.html", timer_data=timer_data, max_session_count=max_session_count)


@main.route("/settings")
def settings():
    return render_template("views/settings.html")