
from flask import request, redirect, url_for, abort
from . import api
from .. import db
from ..utils import TodolistDbHandler


todolistDbHandler = TodolistDbHandler(request, db)


@api.post("/todolist/create")
def add_todolist_item():
    if "todolist-item-add" in request.form:
        value = request.form.get("todolist-item-add")
        if todolistDbHandler.validate(value):
            todolistDbHandler.create(value=value)
            todolistDbHandler.commit_session()
        else:
            abort(400)
    return redirect(url_for("main.index"))
    

@api.post("/todolist/update")
def edit_todolist_item():
    if "todolist-item-edit" in request.form:
        prev_value = request.form.get("todolist-item-edit-prev")
        new_value = request.form.get("todolist-item-edit")
        if todolistDbHandler.validate(new_value):   # prev_value already validated
            todolistDbHandler.edit(prev_value, new_value, "value")
            todolistDbHandler.commit_session()
        else:
            abort(400)
    return redirect(url_for("main.index"))


@api.post("/todolist/delete")
def delete_todolist_item():
    if "todolist-item-delete" in request.form:
        value = request.form.get("todolist-item-delete")
        todolistDbHandler.delete(value=value)
        todolistDbHandler.commit_session()
    return redirect(url_for("main.index"))