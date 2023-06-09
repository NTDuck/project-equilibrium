
from datetime import date
from io import BytesIO

from flask import send_file, request, redirect, url_for, json, flash
from flask_login import login_required, current_user
from sqlalchemy import delete

from . import api
from .. import db
from ..utils import validate_json_data
from ..models import Todolist, TimerSessionCount, ChatbotMessage



@api.get("/user-data/download")
@login_required
def download_user_data():
    # retrieve user data
    todolistItems = getattr(current_user, Todolist.__tablename__)
    todolistData = [getattr(item, "value") for item in todolistItems]

    timerSessionCounts = getattr(current_user, TimerSessionCount.__tablename__)
    timerSessionCountData = [[getattr(item, "date").isoformat(), getattr(item, "session_count")] for item in timerSessionCounts]

    chatbotMessages = getattr(current_user, ChatbotMessage.__tablename__)
    chatbotMessagesData = [[getattr(item, "value"), getattr(item, "type")] for item in chatbotMessages]

    json_data = json.dumps({
        "todolist": todolistData,
        "timer-session-count": timerSessionCountData,
        "chatbot-messages": chatbotMessagesData,
    })

    # create & manipulate in-memory file-like object
    file = BytesIO()
    file.write(json_data.encode("utf-8"))
    file.seek(0)  # Move the file position to the beginning

    file_name = f"pr-eq-export-{date.today()}.json"

    flash(f"user {current_user.username}'s data downloaded as {file_name}")
    
    # Send the file to the client
    return send_file(path_or_file=file, mimetype="application/json", as_attachment=True, download_name=file_name)


@api.get("/user-data/delete")
@login_required
def delete_user_data():
    for table in [Todolist, TimerSessionCount, ChatbotMessage]:
        db.session.execute(delete(table).where(table.user == current_user))
    # note-to-self: send fetch request to frontend to clear localStorage
    db.session.commit()
    flash("data deleted successfully.")
    return redirect(url_for("main.index"))


@api.post("/user-data/upload")
@login_required
def upload_user_data():
    # check if post request has uploaded file
    if "user-data" not in request.files:
        flash("unknown error.")
    
    file = request.files.get("user-data")

    # check if file is valid
    json_data = validate_json_data(file)
    if json_data is None:
        flash("invalid data. please try again.")
        return redirect(url_for("main.index"))

    # handle json data upon validation
    rawTodolistItems = json_data.get("todolist")   # list[str]
    todolistItems = [{"value": value} for value in rawTodolistItems]   # list[dict[str, str]]

    rawTimerSessionCounts = json_data.get("timer-session-count")   # list[list[str, str]]
    timerSessionCounts = [{"date": date.fromisoformat(date_string), "session_count": session_count} for [date_string, session_count] in rawTimerSessionCounts]   # list[dict[str, str]]

    rawChatbotMessages = json_data.get("chatbot-messages")   # list[list[str, str]]
    chatbotMessages = [{"value": value, "type": type} for [value, type] in rawChatbotMessages]   # list[dict[str, str]]

    insert_array = {
        Todolist: todolistItems,
        TimerSessionCount: timerSessionCounts,
        ChatbotMessage: chatbotMessages,
    }

    try:
        for table in insert_array.keys():
            if getattr(current_user, table.__tablename__):
                continue
            for attrs in insert_array.get(table):
                item = table(user=current_user, **attrs)
                db.session.add(item)
    except ValueError:
        flash("invalid data. please try again.")
        return redirect(url_for("main.index"))
    else:
        db.session.commit()
        flash("data uploaded successfully.")
    return redirect(url_for("main.index"))


# warning: since this involves handling unknown files, more security features should be implemented