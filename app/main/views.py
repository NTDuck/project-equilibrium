
from flask import render_template, request
from . import main
from .. import db
from ..utils import TodolistDbHandler, TimerSessionCountDbHandler, ChatbotMessageDbHandler, handle_timer_data


todolistDbHandler = TodolistDbHandler(request, db)
timerSessionCountDbHandler = TimerSessionCountDbHandler(request, db)
chatbotMessageDbHandler = ChatbotMessageDbHandler(request, db)


@main.get("/")
def index():
    return render_template("index.html", todolistItems=todolistDbHandler.handle_db_read(), chatbotMessages=chatbotMessageDbHandler.handle_db_read())


@main.route("/about")
def about():
    return render_template("views/about.html")


@main.get("/stats")
def stats():
    raw_timer_data = timerSessionCountDbHandler.handle_db_read()
    timer_data, max_session_count = handle_timer_data(raw_timer_data)
    return render_template("views/stats.html", timer_data=timer_data, max_session_count=max_session_count)


@main.route("/settings")
def settings():
    return render_template("views/settings.html")