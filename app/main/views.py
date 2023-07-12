
from flask import render_template
from flask_login import current_user, login_required

from config import Config
from . import main
from .. import db
from ..models import User, Todolist, TimerSessionCount, ChatbotMessage


@main.route("/")
def index():
    if current_user.is_authenticated:
        todolistItems = db.session.execute(db.select(Todolist).where(Todolist.user == current_user)).scalars().all()
        # if last msg is user-type, delete it
        chatbotMessages = db.session.execute(db.select(ChatbotMessage).where(ChatbotMessage.user == current_user)).scalars().all()
    else:
        # implement some example messages
        todolistItems = [{"id": ind, "value": val} for ind, val in enumerate(Config.TODOLIST_EXAMPLE_MESSAGES)]
        chatbotMessages = [{"id": ind, "value": val, "type": "user" if ind%2 == 0 else "server"} for ind, val in enumerate(Config.CHATBOT_EXAMPLE_MESSAGES)]
    return render_template("index.html", todolistItems=todolistItems, chatbotMessages=chatbotMessages)


# should be universal regardless of user login state
@main.route("/about")
def about():
    data = {
        "total_users": len(db.session.execute(db.select(User)).scalars().all()),
        "total_pomodoros": sum([getattr(i, "session_count") for i in db.session.execute(db.select(TimerSessionCount)).scalars().all()]),
    }
    return render_template("views/about.html", data=data)


@main.route("/stats")
def stats():
    return render_template("views/stats.html")


@main.route("/settings")
@login_required
def settings():
    return render_template("views/settings.html")