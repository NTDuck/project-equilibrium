
from flask import request, redirect, url_for, jsonify
from . import api
from .. import db
from ..utils import ChatbotMessageDbHandler, text_generation


chatbotMessageDbHandler = ChatbotMessageDbHandler(request, db)


@api.post("/chatbot/server-msg/create")
def generate_server_message():
    if "chatbot-user-msg-input" in request.form:
        user_input = request.form.get("chatbot-user-msg-input").strip()
        chatbotMessageDbHandler.handle_db_insert(user_input, "user")

        server_response = text_generation(user_input)
        chatbotMessageDbHandler.handle_db_insert(server_response, "server")

    return redirect(url_for("main.index"))


@api.post("/chatbot/server-msg/update")
def update_server_message():
    if "chatbot-server-msg-edit" in request.form:
        chatbotMessageDbHandler.server_msg_reload("chatbot-server-msg-edit")
    return redirect(url_for("main.index"))


@api.post("/chatbot/user-msg/update")
def edit_user_message():
    if "chatbot-msg-edit" in request.form:
        chatbotMessageDbHandler.handle_db_update("chatbot-msg-edit-prev", "chatbot-msg-edit")
    return redirect(url_for("main.index"))


@api.post("/chatbot/user-msg/delete")
def delete_user_message():
    if "chatbot-msg-delete" in request.form:
        chatbotMessageDbHandler.handle_db_delete("chatbot-msg-delete")
    return redirect(url_for("main.index"))