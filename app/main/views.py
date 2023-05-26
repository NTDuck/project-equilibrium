
from flask import render_template, request, url_for, redirect
from . import main
from .. import db
from ..utils import DbOperationHandler
from ..models import TodolistItem
from constant import DEFAULT_TODOLIST_ITEM_VALUE


todolistItemEventHandler = DbOperationHandler(request, db, TodolistItem, DEFAULT_TODOLIST_ITEM_VALUE)


@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "todolistItem_add" in request.form:
            todolistItemEventHandler.handle_db_insert("todolistItem_add")
        if "todolistItem_edit" in request.form:
            todolistItemEventHandler.handle_db_update("todolistItem_edit_prev", "todolistItem_edit")
        if "todolistItem_del" in request.form:
            todolistItemEventHandler.handle_db_delete("todolistItem_del")
        return redirect(url_for("main.index"))
    return render_template("index.html", todolistItems=TodolistItem.query.all())


@main.route("/about")
def about():
    return render_template("views/about.html")


@main.route("/stats")
def stats():
    return render_template("views/stats.html")


@main.route("/settings")
def settings():
    return render_template("views/settings.html")