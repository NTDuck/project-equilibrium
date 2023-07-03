
from flask import request, abort, jsonify
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
        try:
            item = Todolist(user=current_user, value=value)
        except ValueError:
            abort(400)
        else:
            db.session.add(item)
            db.session.commit()
    return jsonify({
        "id": item.id if current_user.is_authenticated else 0,
        "value": value,
    })


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
        try:
            item = db.session.execute(db.select(Todolist).filter_by(user=current_user, id=id)).scalar_one()
            setattr(item, "value", value)
        except ValueError:
            return abort(400)
        else:
            db.session.commit()
    return jsonify({})


@api.post("/todolist/delete")
def delete_todolist_item():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if not "id" in data:
        abort(400)
    if current_user.is_authenticated:
        db.session.execute(db.delete(Todolist).where(db.and_(Todolist.user == current_user, Todolist.id == data.get("id"))))
        db.session.commit()
    return jsonify({})