
from datetime import date
from io import BytesIO
from flask import send_file, request, redirect, url_for, abort, json
from flask_login import login_required
from . import api
from .. import todolistDbHandler, timerSessionCountDbHandler, chatbotMessageDbHandler
from ..utils import validate_json_data



@api.get("/user-data/download")
@login_required
def download_user_data():
    # retrieve user data
    todolistItems = todolistDbHandler.read()
    todolistData = [todolistItem.value for todolistItem in todolistItems]

    timerSessionCounts = timerSessionCountDbHandler.read()
    timerSessionCountData = [[timerSessionCount.date.isoformat(), timerSessionCount.session_count] for timerSessionCount in timerSessionCounts]

    chatbotMessages = chatbotMessageDbHandler.read()
    chatbotMessagesData = [[chatbotMessage.value, chatbotMessage.type] for chatbotMessage in chatbotMessages]

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
    
    # Send the file to the client
    return send_file(path_or_file=file, mimetype="application/json", as_attachment=True, download_name=file_name)


@api.get("/user-data/delete")
@login_required
def delete_user_data():
    for dbHandler in [todolistDbHandler, timerSessionCountDbHandler, chatbotMessageDbHandler]:
        dbHandler.delete_all()
    # note-to-self: send fetch request to frontend to clear localStorage
    todolistDbHandler.commit_session()   # could be any dbHandler
    return redirect(url_for("main.index"))


@api.post("/user-data/upload")
@login_required
def upload_user_data():
    # check if post request has uploaded file
    if "user-data" not in request.files:
        abort(400)
    
    file = request.files.get("user-data")

    # check if file is valid
    json_data = validate_json_data(file)
    if json_data is None:
        abort(400)

    # handle json data upon validation
    rawTodolistItems = json_data.get("todolist")   # list[str]
    todolistItems = [{"value": value} for value in rawTodolistItems]   # list[dict[str, str]]
    todolistDbHandler.create_all(todolistItems)

    rawTimerSessionCounts = json_data.get("timer-session-count")   # list[list[str, str]]
    timerSessionCounts = [{"date": date.fromisoformat(date_string), "session_count": session_count} for [date_string, session_count] in rawTimerSessionCounts]   # list[dict[str, str]]
    timerSessionCountDbHandler.create_all(timerSessionCounts)

    rawChatbotMessages = json_data.get("chatbot-messages")   # list[list[str, str]]
    chatbotMessages = [{"value": value, "type": type} for [value, type] in rawChatbotMessages]   # list[dict[str, str]]
    chatbotMessageDbHandler.create_all(chatbotMessages)

    todolistDbHandler.commit_session()   # could be any dbHandler
    return redirect(url_for("main.index"))


# warning: since this involves handling unknown files, more security features should be implemented