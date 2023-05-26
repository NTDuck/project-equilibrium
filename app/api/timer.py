
from flask import jsonify
from config import Config
from . import api


@api.route("/timer-config")
def retrieve_timer_config():
    timer_configs = {
        "work": Config.TIMER_WORK_SESSION_LENGTH,
        "short_break": Config.TIMER_SHORT_BREAK_SESSION_LENGTH,
        "long_break": Config.TIMER_LONG_BREAK_SESSION_LENGTH,
        "interval": Config.TIMER_INTERVAL,
        "delay": Config.TIMER_DELAY,
    }
    return jsonify(timer_configs)