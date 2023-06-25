
from flask import request, abort, jsonify
from flask_login import current_user

from . import api
from .. import db
from ..models import Todolist


@api.post("/todolist/create")
def add_todolist_item():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if not "todolist-item-add" in data:
        abort(400)
    value = data.get("todolist-item-add").strip()
    if current_user.is_authenticated:
        try:
            item = Todolist(user=current_user, value=value)
        except ValueError:
            abort(400)
        else:
            db.session.add(item)
            db.session.commit()
    return jsonify(value)


@api.post("/todolist/update")
def edit_todolist_item():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if not "todolist-item-edit" in data:
        abort(400)
    prev_value = data.get("todolist-item-edit-prev")
    next_value = data.get("todolist-item-edit").strip()
    if current_user.is_authenticated:
        try:
            item = db.session.execute(db.select(Todolist).filter_by(user=current_user, value=prev_value)).scalar_one()
            setattr(item, "value", next_value)
        except ValueError:
            abort(400)
        else:
            db.session.commit()
    return jsonify({
        "todolist-item-edit-prev": prev_value,
        "todolist-item-edit": next_value,
    })


@api.post("/todolist/delete")
def delete_todolist_item():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if not "todolist-item-delete" in data:
        abort(400)
    value = data.get("todolist-item-delete")
    if current_user.is_authenticated:
        db.session.execute(db.delete(Todolist).where(db.and_(Todolist.user == current_user, Todolist.value == value)))
        db.session.commit()
    return jsonify(value)