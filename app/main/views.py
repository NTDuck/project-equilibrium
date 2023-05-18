
from flask import (
    render_template, request, url_for, redirect, 
)

from . import main
from .. import db
from ..models import TodolistItems


@main.route("/", methods=["GET", "POST"])
def index():

    is_data_modified = False

    if request.method == "POST":

        if "todolistItemContent" in request.form:
            todolistItemContent = request.form.get("todolistItemContent")
            if not any([todolistItemContent.isspace(), len(todolistItemContent) == 0]):
                todolistItem_to_add = TodolistItems(value=todolistItemContent)
                db.session.add(todolistItem_to_add)
                is_data_modified = True

        if "todolistItem_del" in request.form:
            todolistItem_del = request.form.get("todolistItem_del")
            todolistItem_to_del = TodolistItems.query.filter_by(value=todolistItem_del).first()
            db.session.delete(todolistItem_to_del)
            is_data_modified = True

        if is_data_modified:
            db.session.commit()
            db.session.close()
            
        return redirect(url_for("main.index"))
    
    return render_template("index.html", todolistItems=TodolistItems.query.all())


@main.route("/about")
def about():
    return render_template("views/about.html")


@main.route("/stats")
def stats():
    return render_template("views/stats.html")


@main.route("/settings")
def settings():
    return render_template("views/settings.html")