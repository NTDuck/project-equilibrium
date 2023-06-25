
from flask import request, abort, jsonify
from flask_login import current_user

from . import api
from .. import db
from ..utils import text_generation
from ..models import ChatbotMessage


@api.post("/chatbot/user-msg/create")
def create_user_message():
    if not request.json:
        abort(400)
    data = request.get_json()
    if not "chatbot-user-msg-create" in data:
        abort(400)
    value = data.get("chatbot-user-msg-create").strip()
    if current_user.is_authenticated:
        try:
            item = ChatbotMessage(user=current_user, value=value, type="user")
        except ValueError:
            abort(400)
        else:
            db.session.add(item)
            db.session.commit()
    return jsonify(value)


@api.post("/chatbot/user-msg/update/<phase>")
def edit_user_message(phase):
    if not request.json:
        abort(400)
    data = request.get_json()

    # might try implementing a dict[str, method]
    if phase == "user":
        if not "chatbot-user-msg-edit" in data:
            abort(400)
        prev_value = data.get("chatbot-user-msg-edit-prev")
        next_value = data.get("chatbot-user-msg-edit").strip()
        if current_user.is_authenticated:
            try:
                item = db.session.execute(db.select(ChatbotMessage).filter_by(user=current_user, value=prev_value)).scalar_one()
                setattr(item, "value", next_value)
                db.session.execute(db.delete(ChatbotMessage).where(db.and_(ChatbotMessage.user == current_user, ChatbotMessage.id >= item.id + 2)))
            except ValueError:
                abort(400)
            else:
                db.session.commit()
        return jsonify(next_value)
    
    elif phase == "server":
        if not "chatbot-server-msg-edit" in data:
            abort(400)
        last_user_msg_value = data.get("chatbot-last-user-msg")
        prev_value = data.get("chatbot-server-msg-edit")
        next_value = text_generation(last_user_msg_value)
        if current_user.is_authenticated:
            try:
                item = db.session.execute(db.select(ChatbotMessage).filter_by(user=current_user, value=prev_value)).scalar_one()
                setattr(item, "value", next_value)
            except ValueError:
                abort(400)
            else:
                db.session.commit()
        return jsonify(next_value)
    else:
        abort(400)


@api.post("/chatbot/user-msg/delete")
def delete_user_message():
    if not request.json:
        abort(400)
    data = request.get_json()
    if not "chatbot-user-msg-delete" in data:
        abort(400)
    value = data.get("chatbot-user-msg-delete")
    if current_user.is_authenticated:
        item = db.session.execute(db.select(ChatbotMessage).filter_by(user=current_user, value=value)).scalar_one()
        db.session.execute(db.delete(ChatbotMessage).where(db.and_(ChatbotMessage.user == current_user, ChatbotMessage.id >= item.id)))
        db.session.commit()
    return jsonify(value)


@api.post("/chatbot/server-msg/create")
def create_server_message():
    if not request.json:
        abort(400)
    data = request.get_json()
    if not "chatbot-server-msg-create" in data:
        abort(400)
    value = data.get("chatbot-server-msg-create").strip()
    server_response = text_generation(value)
    if current_user.is_authenticated:
        try:
            item = ChatbotMessage(user=current_user, value=server_response, type="server")
        except ValueError:
            abort(400)
        else:
            db.session.add(item)
            db.session.commit()
    return jsonify(server_response)


@api.post("/chatbot/server-msg/update")
def update_server_message():
    if not request.json:
        abort(400)
    data = request.get_json()
    if not "chatbot-server-msg-update" in data:
        abort(400)
    # also delete all messages after
    prev_value = data.get("chatbot-server-msg-update")
    if current_user.is_authenticated:
        item = db.session.execute(db.select(ChatbotMessage).filter_by(user=current_user, value=prev_value)).scalar_one()
        db.session.execute(db.delete(ChatbotMessage).where(db.and_(ChatbotMessage.user == current_user, ChatbotMessage.id >= item.id + 1)))

    last_user_msg_value = data.get("chatbot-last-user-msg")
    next_value = text_generation(last_user_msg_value)
    if current_user.is_authenticated:
        try:
            item = db.session.execute(db.select(ChatbotMessage).filter_by(user=current_user, value=prev_value)).scalar_one()
            setattr(item, "value", next_value)
        except ValueError:
            abort(400)
        else:
            db.session.commit()
    return jsonify(next_value)