
import os
from datetime import date
from flask import jsonify, request, abort, session
from flask_login import current_user, login_required

from config import Config
from . import api
from .. import db
from ..models import TimerSessionCount


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
    if "is_timer_ready" not in session:
        session["is_timer_ready"] = True
    if not request.is_json:
        abort(400)
    if not "session-count" in request.json:
        abort(400)
    if current_user.is_authenticated:
        if not session["is_timer_ready"]:
            return jsonify({
                "error": 418,
                "flash": "please wait a few seconds.",
            })
        session["is_timer_ready"] = False
        item = db.session.execute(db.select(TimerSessionCount).where(db.and_(TimerSessionCount.user == current_user, TimerSessionCount.date == date.today()))).scalar_one_or_none()
        try:
            if item is not None:   # query already exists
                session_count = getattr(item, "session_count")
                session_count += 1
                setattr(item, "session_count", session_count)
            else:   # non-existent query
                item = TimerSessionCount(user=current_user, date=date.today(), session_count=1)
                db.session.add(item)
        except ValueError:
            return jsonify({
                "error": 400,
                "flash": "please try again later.",
            })
        else:
            db.session.commit()
            session["is_timer_ready"] = True
    return jsonify({
        "flash": "pomodoro completed.",
    })


@api.get("/timer/session-count/get")
@login_required
def get_timer_session_count():
    timer_session_counts = db.session.execute(db.select(TimerSessionCount).where(TimerSessionCount.user == current_user)).scalars().all()
    return jsonify(timer_session_counts)