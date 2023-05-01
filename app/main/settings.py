
from flask import render_template

from . import main


@main.route("/")
def settings():
    return render_template("settings.html")