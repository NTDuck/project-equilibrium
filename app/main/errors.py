
from random import choice

from flask import render_template
from werkzeug.exceptions import HTTPException

from . import main
from constant import (
    HTTP_STATUS_CODES, GIFS, 
)


@main.app_errorhandler(HTTPException)
def errorhandler(e):
    err = getattr(e, "code", 500)
    title = HTTP_STATUS_CODES[err]["title"]
    description = HTTP_STATUS_CODES[err]["description"]
    gifName = choice(GIFS)
    return render_template("error.html", err=err, title=title, description=description, gifName=gifName), err