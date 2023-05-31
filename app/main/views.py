
from flask import render_template, request
from . import main
from .. import db
from ..utils import TodolistDbHandler, TimerSessionCountDbHandler


todolistDbHandler = TodolistDbHandler(request, db)
timerSessionCountDbHandler = TimerSessionCountDbHandler(request, db)


@main.get("/")
def index():
    return render_template("index.html", todolistItems=todolistDbHandler.handle_db_read())


@main.route("/about")
def about():
    return render_template("views/about.html")


@main.route("/stats")
def stats():
    return render_template("views/stats.html", sessionCounts=timerSessionCountDbHandler.handle_db_read())


@main.route("/settings")
def settings():
    return render_template("views/settings.html")