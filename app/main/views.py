
from flask import render_template

from . import main


# actual objectives
tasks = [
    "focus:outline-none does not work (on MS Edge) # seems hard to solve",
    "needs to work more on error codes & msgs; randomize error svgs",
    "think of a brand icon to put in the navbar",
    "implement a bg-darken-popupmenu for some footer icons",
    "implement basic UI - index.html",
    "streaming the html",
    "add a popup when hover task",
    "write README file",
]
for _ in range(10):
    tasks.append(f"arbitrary value {_}")


@main.route("/")
def index():
    return render_template("index.html", tasks=tasks)


@main.route("/about")
def about():
    return render_template("views/about.html")


@main.route("/stats")
def stats():
    return render_template("views/stats.html")


@main.route("/settings")
def settings():
    return render_template("views/settings.html")