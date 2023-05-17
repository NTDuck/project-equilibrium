
from flask import (
    render_template, request, url_for, redirect, session, 
)

from . import main
from constant import TODOLIST_ITEMS


@main.route("/", methods=["GET", "POST"])
def index():

    session["todolistItems"] = TODOLIST_ITEMS

    if request.method == "POST":

        todolistItemContent = request.form.get("todolistItemContent", "")
        if not all([i.isspace() for i in todolistItemContent]):   # only append non-empty strings
            session["todolistItems"].append(todolistItemContent)
        
        return redirect(url_for("main.index", todolistItems=session.get("todolistItems")))
    
    return render_template("index.html", todolistItems=session.get("todolistItems"))


@main.route("/about")
def about():
    return render_template("views/about.html")


@main.route("/stats")
def stats():
    return render_template("views/stats.html")


@main.route("/settings")
def settings():
    return render_template("views/settings.html")