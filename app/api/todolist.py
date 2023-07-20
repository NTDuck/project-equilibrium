
from flask import request, abort, jsonify, session
from flask_login import current_user

from . import api
from .. import db
from ..models import Todolist


@api.post("/todolist/create")
def create_todolist_item():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if not "todolist-create" in data:
        abort(400)
    value = data.get("todolist-create").strip()
    if current_user.is_authenticated:
        if not session["is_todolist_ready"]:
            response = {"error": 418}
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                response.update({"flash": "please wait a few seconds.",})
            return jsonify(response)
        session["is_todolist_ready"] = False
        try:
            item = Todolist(user=current_user, value=value)
        except ValueError:
            response = {"error": 400}
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                response.update({"flash": "item invalid. please try again."})
            return jsonify(response)
        else:
            db.session.add(item)
            db.session.commit()
            session["is_todolist_ready"] = True
    response = {
        "id": item.id if current_user.is_authenticated else 0,
        "value": value,
    }
    if session["settings"]["NOTIFICATIONS_TODOLIST"]:
        response.update({"flash": "item created."})
    return jsonify(response)


@api.post("/todolist/update")
def update_todolist_item():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if not "todolist-update" in data and not "id" in data:
        abort(400)
    id = data.get("id")
    value = data.get("todolist-update").strip()
    if current_user.is_authenticated:
        if not session["is_todolist_ready"]:
            response = {"error": 418}
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                response.update({"flash": "please wait a few seconds."})
            return jsonify(response)
        session["is_todolist_ready"] = False
        try:
            item = db.session.execute(db.select(Todolist).where(db.and_(Todolist.user == current_user, Todolist.id == id))).scalar_one_or_none()
            if item is None:   # practically cannot occur
                abort(400)
            setattr(item, "value", value)
        except ValueError:
            response = {"error": 400}
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                response.update({"flash": "item invalid. please try again."})
            return jsonify(response)
        else:
            db.session.commit()
            session["is_todolist_ready"] = True
    response = {}
    if session["settings"]["NOTIFICATIONS_TODOLIST"]:
        response.update({"flash": "item updated."})
    return jsonify(response)


@api.post("/todolist/delete")
def delete_todolist_item():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if not "id" in data:
        abort(400)
    if current_user.is_authenticated:
        if not session["is_todolist_ready"]:
            response = {"error": 418}
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                response.update({"flash": "please wait a few seconds."})
            return jsonify(response)
        session["is_todolist_ready"] = False
        db.session.execute(db.delete(Todolist).where(db.and_(Todolist.user == current_user, Todolist.id == data.get("id"))))
        db.session.commit()
        session["is_todolist_ready"] = True
    response = {}
    if session["settings"]["NOTIFICATIONS_TODOLIST"]:
        response.update({"flash": "item deleted."})
    return jsonify(response)