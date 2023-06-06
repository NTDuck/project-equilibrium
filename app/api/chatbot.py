
from flask import request, redirect, url_for, abort
from . import api
from .. import db
from ..utils import ChatbotMessageDbHandler, text_generation


chatbotMessageDbHandler = ChatbotMessageDbHandler(request, db)


@api.post("/chatbot/server-msg/create")
def generate_server_message():
    if "chatbot-user-msg-input" in request.form:
        user_input = request.form.get("chatbot-user-msg-input").strip()
        if chatbotMessageDbHandler.validate(user_input):
            chatbotMessageDbHandler.create(value=user_input, type="user")
            # text generation
            server_response = text_generation(user_input)
            if chatbotMessageDbHandler.validate(server_response, max_str_length=512):
                chatbotMessageDbHandler.create(value=server_response, type="server")
                chatbotMessageDbHandler.commit_session()
        else:
            abort(400)
    return redirect(url_for("main.index"))


@api.post("/chatbot/server-msg/update")
def update_server_message():
    if "chatbot-server-msg-edit" in request.form:
        value = request.form.get("chatbot-server-msg-edit")
        chatbotMessageDbHandler.edit_server_msg(value)
        chatbotMessageDbHandler.commit_session()
    return redirect(url_for("main.index"))


@api.post("/chatbot/user-msg/update")
def edit_user_message():
    if "chatbot-msg-edit" in request.form:
        prev_value = request.form.get("chatbot-msg-edit-prev")
        new_value = request.form.get("chatbot-msg-edit")
        if chatbotMessageDbHandler.validate(new_value):
            chatbotMessageDbHandler.edit_user_msg(prev_value, new_value)
            chatbotMessageDbHandler.commit_session()
        else:
            abort(400)
    return redirect(url_for("main.index"))


@api.post("/chatbot/user-msg/delete")
def delete_user_message():
    if "chatbot-msg-delete" in request.form:
        value = request.form.get("chatbot-msg-delete")
        chatbotMessageDbHandler.delete(value)
        chatbotMessageDbHandler.commit_session()
    return redirect(url_for("main.index"))