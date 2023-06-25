
from flask import render_template
from flask_login import current_user, login_required

from . import main
from ..utils import handle_timer_data
from ..models import Todolist, TimerSessionCount, ChatbotMessage
from config import Config


@main.route("/")
def index():
    if current_user.is_authenticated:
        todolistItems = getattr(current_user, Todolist.__tablename__)
        chatbotMessages = getattr(current_user, ChatbotMessage.__tablename__)
    else:
        # implement some example messages
        todolistItems = [{"value": i} for i in Config.TODOLIST_EXAMPLE_MESSAGES]
        chatbotMessages = [{"value": i, "type": "user" if Config.CHATBOT_EXAMPLE_MESSAGES.index(i)%2 == 0 else "server"} for i in Config.CHATBOT_EXAMPLE_MESSAGES]
    return render_template("index.html", todolistItems=todolistItems, chatbotMessages=chatbotMessages)


# should be universal regardless of user login state
@main.route("/about")
def about():
    return render_template("views/about.html")


@main.route("/stats")
@login_required
def stats():
    raw_timer_data = getattr(current_user, TimerSessionCount.__tablename__)
    timer_data, max_session_count = handle_timer_data(raw_timer_data)
    return render_template("views/stats.html", timer_data=timer_data, max_session_count=max_session_count)


@main.route("/settings")
@login_required
def settings():
    return render_template("views/settings.html")