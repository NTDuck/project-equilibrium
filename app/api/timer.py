
import os
from flask import jsonify, request
from config import Config
from . import api


@api.get("/timer-config")
def get_timer_config():
    timer_configs = {
        "work": Config.TIMER_WORK_SESSION_LENGTH,
        "short_break": Config.TIMER_SHORT_BREAK_SESSION_LENGTH,
        "long_break": Config.TIMER_LONG_BREAK_SESSION_LENGTH,
        "interval": Config.TIMER_INTERVAL,
        "delay": Config.TIMER_DELAY,
    }
    return jsonify(timer_configs)


@api.get("/timer-image-files/<folder>")
def get_timer_gifs(folder):
    timer_display_image_files = os.listdir(os.path.join(os.path.dirname(__file__), f"../static/images/gifs/timer/{folder}/"))
    return jsonify(timer_display_image_files)