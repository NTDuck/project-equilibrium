
import json
from datetime import date
from io import BytesIO
from flask import send_file, request, redirect, url_for
from . import api
from .. import db
from config import Config
from ..utils import TodolistDbHandler, is_file_allowed


todolistItemEventHandler = TodolistDbHandler(request, db)


@api.get("/download-user-data")
def download_user_data():
    # retrieve user data
    todolistItems = todolistItemEventHandler.handle_db_read()
    todolist_data = [todolistItem.value for todolistItem in todolistItems]
    json_data = json.dumps({
        "todolist": todolist_data,
        "foo": "bar",
    })

    # create & manipulate in-memory file-like object
    file = BytesIO()
    file.write(json_data.encode("utf-8"))
    file.seek(0)  # Move the file position to the beginning

    file_name = f"pr-eq-export-{date.today()}.json"
    
    # Send the file to the client
    return send_file(path_or_file=file, mimetype="application/json", as_attachment=True, download_name=file_name)


@api.get("/delete-user-data")
def delete_user_data():
    download_user_data()
    todolistItemEventHandler.delete_table()
    return redirect(url_for("main.index"))


@api.post("/upload-user-data")
def upload_user_data():
    # check if post request has uploaded file
    if "user-data" not in request.files:
        # flash a message
        return redirect(url_for("main.index"))
    
    file = request.files.get("user-data")

    # check if file is empty
    # warning: event never received, error might occur in production
    if file.filename == "":
        # flash a message
        return redirect(url_for("main.index"))
    
    # check if file is .json
    if file and is_file_allowed(file.filename, Config.ALLOWED_FILE_EXTENSIONS_USER_DATA):
        file_content = file.read()
        json_data = json.loads(file_content)

        # handle json data
        if all((
            not todolistItemEventHandler.handle_db_read(),   # only execute if table is empty
            json_data.keys() == {"todolist", "foo"},

        )):
            todolistItems = json_data.get("todolist")
            todolistItemEventHandler.handle_db_multiple_insert(todolistItems)
    
    return redirect(url_for("main.index"))


# warning: since this involves handling unknown files, more security features should be implemented