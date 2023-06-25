
import os
from datetime import date

from flask import json
from transformers import pipeline

from config import Config


def is_file_allowed(filename, allowed_file_exts) -> bool:
    filetype = os.path.splitext(filename)[-1]
    return filetype in allowed_file_exts


def validate_json_data(file) -> dict | None:
    # check if file is empty
    # warning: event never received, error might occur in production
    if any([
        file.filename == "",
        not is_file_allowed(file.filename, Config.USER_DATA_ALLOWED_FILE_EXTENSIONS),
    ]):
        return None
    
    file_content = file.read()
    json_data = json.loads(file_content)
    
    # check if data is readable dict
    if any([
        not isinstance(json_data, dict),
        json_data.keys() != {"todolist", "timer-session-count", "chatbot-messages"},
    ]):
        return None
    
    # check if data.todolist contains only valid values
    todolists = json_data.get("todolist")
    if len(todolists) != len(set(todolists)):
        return None
    
    timer_session_counts = json_data.get("timer-session-count")
    date_strings = [item[0] for item in timer_session_counts]
    if len(date_strings) != len(set(date_strings)):
        return None
    try:
        for date_string in date_strings:
            date.fromisoformat(date_string)   # check if date_string is stored in valid iso format
    except ValueError:   # raised if date_string is not in valid iso format
        return None

    chatbot_messages = json_data.get("chatbot-messages")
    values = [item[0] for item in chatbot_messages]
    types = [item[1] for item in chatbot_messages]

    if len(values) != len(set(values)):
        return None
    if any([
        # check if types follows pattern ["user", "server"] if not empty
        all([
            set(types) != {"user", "server"},
            not types,
        ]),
        types != ["user", "server"] * (len(types) // 2)
    ]):
        return None
    
    # upon validation
    return json_data


def handle_timer_data(data):
    if not data:
        return [], 1
    item_session_counts = [item.session_count for item in data]
    timer_data = [[item.date.strftime("%b"), item.date.strftime("%d"), item.session_count] for item in data]
    return timer_data, max(item_session_counts)


# warning: should run on multiple threads
def text_generation(input_text: str) -> str:
    generator = pipeline("text-generation", model=Config.HUGGINGFACE_MODEL)
    res = generator(
        input_text,
        min_length=Config.HUGGINGFACE_MODEL_MIN_LENGTH,
        max_length=Config.HUGGINGFACE_MODEL_MAX_LENGTH,
    )
    return res[0].get("generated_text").strip().replace("\n", "")


"""
note-to-self: will need to implement task queue with celery + redis: https://stackabuse.com/asynchronous-tasks-using-flask-redis-and-celery/

TODOLIST:
- implement daily mail count to avoid being locked out of account (cap: 2000)
- password reset (via gmail)
- password update (direct)
"""