
from flask import request, redirect, url_for
from . import api
from .. import db
from ..utils import TodolistDbHandler


todolistDbHandler = TodolistDbHandler(request, db)


@api.post("/add-todolist-item")
def add_todolist_item():
    if "todolist-item-add" in request.form:
        todolistDbHandler.handle_db_insert("todolist-item-add")
    return redirect(url_for("main.index"))
    

@api.post("/edit-todolist-item")
def edit_todolist_item():
    if "todolist-item-edit" in request.form:
        todolistDbHandler.handle_db_update("todolist-item-edit-prev", "todolist-item-edit")
    return redirect(url_for("main.index"))


@api.post("/delete-todolist-item")
def delete_todolist_item():
    if "todolist-item-delete" in request.form:
        todolistDbHandler.handle_db_delete("todolist-item-delete")
    return redirect(url_for("main.index"))