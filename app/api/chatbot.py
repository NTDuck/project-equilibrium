
from flask import request, abort, jsonify
from flask_login import current_user

from . import api
from .. import chatbotMessageDbHandler
from ..utils import text_generation


@api.post("/chatbot/user-msg/create")
def create_user_message():
    if not request.json:
        abort(400)
    data = request.get_json()
    if "chatbot-user-msg-create" in data:
        value = data.get("chatbot-user-msg-create").strip()
        if current_user.is_authenticated:
            if not chatbotMessageDbHandler.validate(value):
                abort(400)
            chatbotMessageDbHandler.create(value=value, type="user")
            chatbotMessageDbHandler.commit_session()
        return jsonify(value)


@api.post("/chatbot/user-msg/update/<phase>")
def edit_user_message(phase):
    if not request.json:
        abort(400)
    data = request.get_json()
    if phase == "user":
        if "chatbot-user-msg-edit" in data:
            prev_value = data.get("chatbot-user-msg-edit-prev")
            new_value = data.get("chatbot-user-msg-edit")
            if current_user.is_authenticated:
                if not chatbotMessageDbHandler.validate(new_value):   # assume prev_value already validated
                    abort(400)
                chatbotMessageDbHandler.delete(prev_value, ignore_items_from_self=2)
                chatbotMessageDbHandler.edit(prev_value, new_value, "value")
                chatbotMessageDbHandler.commit_session()
            return jsonify(new_value)
    elif phase == "server":
        if "chatbot-server-msg-edit" in data:
            last_user_msg_value = data.get("chatbot-last-user-msg")
            prev_value = data.get("chatbot-server-msg-edit")
            new_value = text_generation(last_user_msg_value)
            if current_user.is_authenticated:
                if not chatbotMessageDbHandler.validate(new_value, max_str_length=512):
                    abort(400)
                chatbotMessageDbHandler.edit(prev_value, new_value, "value")
                chatbotMessageDbHandler.commit_session()
            return jsonify(new_value)


@api.post("/chatbot/user-msg/delete")
def delete_user_message():
    if not request.json:
        abort(400)
    data = request.get_json()
    if "chatbot-user-msg-delete" in data:
        value = data.get("chatbot-user-msg-delete")
        if current_user.is_authenticated:
            chatbotMessageDbHandler.delete(value)
            chatbotMessageDbHandler.commit_session()
        return jsonify(value)


@api.post("/chatbot/server-msg/create")
def create_server_message():
    if not request.json:
        abort(400)
    data = request.get_json()
    if "chatbot-server-msg-create" in data:
        value = data.get("chatbot-server-msg-create").strip()
        server_response = text_generation(value)
        if current_user.is_authenticated:
            if not chatbotMessageDbHandler.validate(server_response, max_str_length=512):
                abort(400)
            chatbotMessageDbHandler.create(value=server_response, type="server")
            chatbotMessageDbHandler.commit_session()
        return jsonify(server_response)


@api.post("/chatbot/server-msg/update")
def update_server_message():
    if not request.json:
        abort(400)
    data = request.get_json()
    if "chatbot-server-msg-update" in data:
        # also delete all messages after
        prev_value = data.get("chatbot-server-msg-update")
        if current_user.is_authenticated:
            chatbotMessageDbHandler.delete(prev_value, ignore_items_from_self=1)

        last_user_msg_value = data.get("chatbot-last-user-msg")
        new_value = text_generation(last_user_msg_value)
        if current_user.is_authenticated:
            if not chatbotMessageDbHandler.validate(new_value, max_str_length=512):
                abort(400)
            chatbotMessageDbHandler.edit(prev_value, new_value, "value")
            chatbotMessageDbHandler.commit_session()
        return jsonify(new_value)