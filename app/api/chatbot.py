
from flask import request, abort, jsonify, session
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
            if not session["is_chatbot_ready"]:
                response = {"error": 418}
                if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                    response.update({"flash": "please wait a few seconds."})
                return jsonify(response)
            session["is_chatbot_ready"] = False
            item = ChatbotMessage(user=current_user, value=value, type="user")
        except ValueError:
            response = {"error": 400}
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                response.update({"flash": "item invalid. please try again."})
            return jsonify(response)
        else:
            db.session.add(item)
            db.session.commit()
    response = {
        "id": item.id if current_user.is_authenticated else 0,
        "value": value,
    }
    if session["settings"]["NOTIFICATIONS_CHATBOT"]:
        response.update({"flash": "chatbot user message created."})
    return jsonify(response)


@api.post("/chatbot/user-msg/update/<phase>")
def edit_user_message(phase):
    if not request.json:
        abort(400)
    data = request.get_json()

    # might try implementing a dict[str, method]
    if phase == "user":
        if not session["is_chatbot_ready"]:
            response = {"error": 418}
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                response.update({"flash": "please wait a few seconds."})
            return jsonify(response)
        session["is_chatbot_ready"] = False
        if not "chatbot-user-msg-update" in data and not "id" in data:
            abort(400)
        user_msg_id = data.get("id")
        user_msg_value = data.get("chatbot-user-msg-update").strip()
        if current_user.is_authenticated:
            try:
                item = db.session.execute(db.select(ChatbotMessage).where(db.and_(ChatbotMessage.user == current_user, ChatbotMessage.id == user_msg_id))).scalar_one_or_none()
                if item is None:
                    abort(400)
                setattr(item, "value", user_msg_value)
                db.session.execute(db.delete(ChatbotMessage).where(db.and_(ChatbotMessage.user == current_user, ChatbotMessage.id >= item.id + 2)))
            except ValueError:
                response = {"error": 400}
                if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                    response.update({"flash": "item invalid. please try again."})
                return jsonify(response)
            else:
                db.session.commit()
        response = {}
        if session["settings"]["NOTIFICATIONS_CHATBOT"]:
            response.update({"flash": "chatbot user message updated."})
        return jsonify(response)
    
    elif phase == "server":
        if not "chatbot-user-msg-last" in data and not "id" in data:
            abort(400)
        server_msg_id = data.get("id")
        user_msg_last_value = data.get("chatbot-user-msg-last")
        server_msg_next_value = text_generation(user_msg_last_value)
        print(server_msg_id, user_msg_last_value, server_msg_next_value)
        if current_user.is_authenticated:
            try:
                item = db.session.execute(db.select(ChatbotMessage).where(db.and_(ChatbotMessage.user == current_user, ChatbotMessage.id == server_msg_id))).scalar_one_or_none()
                if item is None:
                    abort(400)
                setattr(item, "value", server_msg_next_value)
            except ValueError:
                response = {"error": 400}
                if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                    response.update({"flash": "item invalid. please try again."})
                return jsonify(response)
            else:
                db.session.commit()
                session["is_chatbot_ready"] = True
        response = {"value": server_msg_next_value}
        if session["settings"]["NOTIFICATIONS_CHATBOT"]:
            response.update({"flash": "chatbot server message updated."})
        return jsonify(response)
    else:
        abort(400)


@api.post("/chatbot/user-msg/delete")
def delete_user_message():
    if not request.json:
        abort(400)
    data = request.get_json()
    if not "id" in data:
        abort(400)
    id = data.get("id")
    if current_user.is_authenticated:
        if not session["is_chatbot_ready"]:
            response = {"error": 418}
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                response.update({"flash": "please wait a few seconds."})
            return jsonify(response)
        session["is_chatbot_ready"] = False
        db.session.execute(db.delete(ChatbotMessage).where(db.and_(ChatbotMessage.user == current_user, ChatbotMessage.id >= id)))
        db.session.commit()
        session["is_chatbot_ready"] = True
    response = {}
    if session["settings"]["NOTIFICATIONS_CHATBOT"]:
        response.update({"flash": "chatbot user message deleted."})
    return jsonify(response)


@api.post("/chatbot/server-msg/create")
def create_server_message():
    if not request.json:
        abort(400)
    data = request.get_json()
    if not "chatbot-server-msg-create" in data:
        abort(400)
    value = data.get("chatbot-server-msg-create").strip()
    server_msg_value = text_generation(value)
    if current_user.is_authenticated:
        try:
            item = ChatbotMessage(user=current_user, value=server_msg_value, type="server")
        except ValueError:
            response = {"error": 400}
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                response.update({"flash": "item invalid. please try again."})
            return jsonify(response)
        else:
            db.session.add(item)
            db.session.commit()
            session["is_chatbot_ready"] = True
    response = {
        "id": item.id,
        "value": server_msg_value,
    }
    if session["settings"]["NOTIFICATIONS_CHATBOT"]:
        response.update({"flash": "chatbot server message created."})
    return jsonify(response)


@api.post("/chatbot/server-msg/update")
def update_server_message():
    if not session["is_chatbot_ready"]:
        response = {"error": 418}
        if session["settings"]["NOTIFICATIONS_SYSTEM"]:
            response.update({"flash": "please wait a few seconds."})
        return jsonify(response)
    session["is_chatbot_ready"] = False
    if not request.json:
        abort(400)
    data = request.get_json()
    if not "id" in data or not "chatbot-user-msg-last" in data:
        abort(400)
    # also delete all messages after
    id = data.get("id")
    if current_user.is_authenticated:
        item = db.session.execute(db.select(ChatbotMessage).where(db.and_(ChatbotMessage.user == current_user, ChatbotMessage.id == id))).scalar_one_or_none()
        if item is None:
            response = {"error": 400}
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                response.update({"flash": "item invalid. please try again."})
            return jsonify(response)
        db.session.execute(db.delete(ChatbotMessage).where(db.and_(ChatbotMessage.user == current_user, ChatbotMessage.id >= item.id + 1)))

    user_msg_last_value = data.get("chatbot-user-msg-last")
    server_msg_next_value = text_generation(user_msg_last_value)
    if current_user.is_authenticated:
        try:
            setattr(item, "value", server_msg_next_value)
        except ValueError:
            response = {"error": 400}
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                response.update({"flash": "item invalid. please try again."})
            return jsonify(response)
        else:
            db.session.commit()
            session["is_chatbot_ready"] = True
    response = {"value": server_msg_next_value}
    if session["settings"]["NOTIFICATIONS_CHATBOT"]:
        response.update({"flash": "chatbot server message updated."})
    return jsonify(response)