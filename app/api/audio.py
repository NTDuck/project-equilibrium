
import os
from flask import jsonify
from . import api


@api.route("/audio-files/<folder>")
def get_audio_files(folder):
    audio_files = os.listdir(os.path.join(os.path.dirname(__file__), f"../static/audio/{folder}/"))
    return jsonify(audio_files)