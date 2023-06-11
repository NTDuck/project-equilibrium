
import os
import random

from flask import render_template
from werkzeug.exceptions import HTTPException

from . import main


@main.app_errorhandler(HTTPException)
def errorhandler(e):
    err = getattr(e, "code", 500)
    err_name = getattr(e, "name", "something went wrong").lower()
    gif_name = random.choice(os.listdir(os.path.join(os.path.dirname(__file__), "../static/images/gifs/error")))
    return render_template("error.html", err=err, err_name=err_name, gif_name=gif_name), err