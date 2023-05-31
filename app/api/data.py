
import json
from datetime import date
from io import BytesIO
from flask import send_file, request, redirect, url_for, abort
from . import api
from .. import db
from config import Config
from ..utils import TodolistDbHandler, TimerSessionCountDbHandler, validate_json_data


todolistDbHandler = TodolistDbHandler(request, db)
timerSessionCountDbHandler = TimerSessionCountDbHandler(request, db)


@api.get("/download-user-data")
def download_user_data():
    # retrieve user data
    todolistItems = todolistDbHandler.handle_db_read()
    todolistData = [todolistItem.value for todolistItem in todolistItems]

    timerSessionCounts = timerSessionCountDbHandler.handle_db_read()
    timerSessionCountData = [[timerSessionCount.date.isoformat(), timerSessionCount.session_count] for timerSessionCount in timerSessionCounts]

    json_data = json.dumps({
        "todolist": todolistData,
        "timer-session-count": timerSessionCountData,
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
    todolistDbHandler.delete_table()
    timerSessionCountDbHandler.delete_table()
    return redirect(url_for("main.index"))


@api.post("/upload-user-data")
def upload_user_data():
    # check if post request has uploaded file
    if "user-data" not in request.files:
        abort(400)
    
    file = request.files.get("user-data")

    # check if file is valid
    json_data = validate_json_data(file)
    if not json_data:
        abort(400)

    # handle json data upon validation
    todolistItems = json_data.get("todolist")
    todolistDbHandler.handle_db_multiple_insert(todolistItems)

    rawTimerSessionCounts = json_data.get("timer-session-count")
    timerSessionCounts = [[date.fromisoformat(date_string), session_count] for [date_string, session_count] in rawTimerSessionCounts]
    timerSessionCountDbHandler.handle_db_multiple_insert(timerSessionCounts)
    
    return redirect(url_for("main.index"))


# warning: since this involves handling unknown files, more security features should be implemented