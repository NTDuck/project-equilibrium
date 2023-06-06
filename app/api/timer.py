
import os
from datetime import date
from flask import jsonify, request, redirect, url_for

from config import Config
from . import api
from .. import db
from ..utils import TimerSessionCountDbHandler
from ..models import TimerSessionCount


timerSessionCountDbHandler = TimerSessionCountDbHandler(request, db)


@api.get("/timer/config")
def get_timer_config():
    timer_configs = {
        "work": Config.TIMER_WORK_SESSION_LENGTH,
        "short_break": Config.TIMER_SHORT_BREAK_SESSION_LENGTH,
        "long_break": Config.TIMER_LONG_BREAK_SESSION_LENGTH,
        "interval": Config.TIMER_INTERVAL,
        "delay": Config.TIMER_DELAY,
    }
    return jsonify(timer_configs)


@api.get("/timer/image-files/<folder>")
def get_timer_gifs(folder):
    timer_display_image_files = os.listdir(os.path.join(os.path.dirname(__file__), f"../static/images/gifs/timer/{folder}/"))
    return jsonify(timer_display_image_files)


@api.post("/timer/session-count/update")
def update_timer_session_count():
    if "session-count" in request.json:
        item = TimerSessionCount.query.filter_by(date=date.today()).first()
        if item is not None:   # query already exists
            timerSessionCountDbHandler.edit(item)
        else:   # non-existent query
            timerSessionCountDbHandler.create(date=date.today(), session_count=1)
        timerSessionCountDbHandler.commit_session()
    return redirect(url_for("main.index"))   # server returns 500 otherwise


@api.get("/timer/session-count/get")
def get_timer_session_count():
    timer_session_counts = timerSessionCountDbHandler.read()   # list[list[str, int]]
    return jsonify(timer_session_counts)