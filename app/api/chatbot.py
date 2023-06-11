
from flask import request, redirect, url_for, abort, jsonify
from . import api
from .. import db
from ..utils import ChatbotMessageDbHandler, text_generation


chatbotMessageDbHandler = ChatbotMessageDbHandler(request, db)


@api.post("/chatbot/user-msg/create")
def create_user_message():
    if request.json:
        data = request.get_json()
        if "chatbot-user-msg-create" in data:
            value = data.get("chatbot-user-msg-create").strip()
            if chatbotMessageDbHandler.validate(value):
                chatbotMessageDbHandler.create(value=value, type="user")
                chatbotMessageDbHandler.commit_session()
                return jsonify(value)
            else:
                abort(400)
    return redirect(url_for("main.index"))


@api.post("/chatbot/user-msg/update/<phase>")
def edit_user_message(phase):
    if request.json:
        data = request.get_json()
        if phase == "user":
            if "chatbot-user-msg-edit" in data:
                prev_value = data.get("chatbot-user-msg-edit-prev")
                new_value = data.get("chatbot-user-msg-edit")
                if chatbotMessageDbHandler.validate(new_value):   # assume prev_value already validated
                    chatbotMessageDbHandler.delete(prev_value, ignore_items_from_self=2)
                    chatbotMessageDbHandler.edit(prev_value, new_value, "value")
                    chatbotMessageDbHandler.commit_session()
                    return jsonify(new_value)
                else:
                    abort(400)
        elif phase == "server":
            if "chatbot-server-msg-edit" in data:
                last_user_msg_value = data.get("chatbot-last-user-msg")
                prev_value = data.get("chatbot-server-msg-edit")
                new_value = text_generation(last_user_msg_value)
                chatbotMessageDbHandler.edit(prev_value, new_value, "value")
                chatbotMessageDbHandler.commit_session()
                return jsonify(new_value)
            else:
                abort(400)
    return redirect(url_for("main.index"))


@api.post("/chatbot/user-msg/delete")
def delete_user_message():
    if request.json:
        data = request.get_json()
        if "chatbot-user-msg-delete" in data:
            value = data.get("chatbot-user-msg-delete")
            chatbotMessageDbHandler.delete(value)
            chatbotMessageDbHandler.commit_session()
            return jsonify(value)
        else:
            abort(400)
    return redirect(url_for("main.index"))


@api.post("/chatbot/server-msg/create")
def create_server_message():
    if request.json:
        data = request.get_json()
        if "chatbot-server-msg-create" in data:
            value = data.get("chatbot-server-msg-create").strip()
            server_response = text_generation(value)
            if chatbotMessageDbHandler.validate(server_response, max_str_length=512):
                chatbotMessageDbHandler.create(value=server_response, type="server")
                chatbotMessageDbHandler.commit_session()
                return jsonify(server_response)
            else:
                abort(400)
    return redirect(url_for("main.index"))


@api.post("/chatbot/server-msg/update")
def update_server_message():
    if request.json:
        data = request.get_json()
        if "chatbot-server-msg-update" in data:
            # also delete all messages after
            prev_value = data.get("chatbot-server-msg-update")
            chatbotMessageDbHandler.delete(prev_value, ignore_items_from_self=1)

            last_user_msg_value = data.get("chatbot-last-user-msg")
            new_value = text_generation(last_user_msg_value)
            chatbotMessageDbHandler.edit(prev_value, new_value, "value")

            chatbotMessageDbHandler.commit_session()
            return jsonify(new_value)
        else:
            abort(400)
    return redirect(url_for("main.index"))