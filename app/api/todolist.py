
from flask import request, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user
from . import api
from .. import db
from ..utils import TodolistDbHandler


todolistDbHandler = TodolistDbHandler(request, db)
    

@api.post("/todolist/create")
@login_required
def add_todolist_item():
    if request.is_json:
        data = request.get_json()
        if "todolist-item-add" in data:
            value = data.get("todolist-item-add")
            if todolistDbHandler.validate(value):
                if current_user.is_authenticated:
                    todolistDbHandler.create(value=value)
                    todolistDbHandler.commit_session()
                return jsonify(value)
            else:
                abort(400)
    return redirect(url_for("main.index"))


@api.post("/todolist/update")
@login_required
def edit_todolist_item():
    if request.is_json:
        data = request.get_json()
        if "todolist-item-edit" in data:
            prev_value = data.get("todolist-item-edit-prev")
            new_value = data.get("todolist-item-edit")
            if todolistDbHandler.validate(new_value):   # prev_value already validated
                if current_user.is_authenticated:
                    todolistDbHandler.edit(prev_value, new_value, "value")
                    todolistDbHandler.commit_session()
                return jsonify({
                    "todolist-item-edit-prev": prev_value,
                    "todolist-item-edit": new_value,
                })
            else:
                abort(400)
    return redirect(url_for("main.index"))


@api.post("/todolist/delete")
@login_required
def delete_todolist_item():
    if request.is_json:
        data = request.get_json()
        if "todolist-item-delete" in data:
            value = data.get("todolist-item-delete")
            if current_user.is_authenticated:
                todolistDbHandler.delete(value=value)
                todolistDbHandler.commit_session()
            return jsonify(value)
        else:
            abort(400)
    return redirect(url_for("main.index"))