
from flask import request, abort, jsonify
from flask_login import current_user
from . import api
from .. import todolistDbHandler


@api.post("/todolist/create")
def add_todolist_item():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if "todolist-item-add" in data:
        value = data.get("todolist-item-add")
        if current_user.is_authenticated:
            if not todolistDbHandler.validate(value):
                abort(400)
            todolistDbHandler.create(value=value)
            todolistDbHandler.commit_session()
        return jsonify(value)


@api.post("/todolist/update")
def edit_todolist_item():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if "todolist-item-edit" in data:
        prev_value = data.get("todolist-item-edit-prev")
        new_value = data.get("todolist-item-edit")
        if current_user.is_authenticated:
            if not todolistDbHandler.validate(new_value):   # prev_value already validated
                abort(400)
            todolistDbHandler.edit(prev_value, new_value, "value")
            todolistDbHandler.commit_session()
        return jsonify({
                "todolist-item-edit-prev": prev_value,
                "todolist-item-edit": new_value,
            })


@api.post("/todolist/delete")
def delete_todolist_item():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if "todolist-item-delete" in data:
        value = data.get("todolist-item-delete")
        if current_user.is_authenticated:
            todolistDbHandler.delete(value=value)
            todolistDbHandler.commit_session()
        return jsonify(value)