
from flask import render_template, session, request, redirect, url_for, flash
from flask_login import current_user, login_required

from config import Config
from . import main
from .. import db
from ..models import User, Todolist, TimerSessionCount, ChatbotMessage


@main.before_app_request
def populate_session():
    if "is_first_request" in session:
        return
    session.update({
        "settings": {key: getattr(current_user, key.lower()) for key in Config.DEFAULT_SETTINGS.keys()} if current_user.is_authenticated else {key: item["value"] for key, item in Config.DEFAULT_SETTINGS.items()},
        "is_settings_changed": False,
        "is_todolist_ready": True,
        "is_timer_ready": True,
        "is_chatbot_ready": True,
        "is_first_request": False,
    })

# must include response as param & return response
@main.after_request
def register_settings(response):
    if not session["is_settings_changed"]:
        return response
    session.update({
        "settings": {key: getattr(current_user, key.lower()) for key in Config.DEFAULT_SETTINGS.keys()} if current_user.is_authenticated else {key: item["value"] for key, item in Config.DEFAULT_SETTINGS.items()},
        "is_settings_changed": False,
    })
    return response


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


@main.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        data = {key: int(request.form.get(key)) for key in Config.DEFAULT_SETTINGS.keys()}
        current_settings = {key: int(getattr(current_user, key.lower())) for key in Config.DEFAULT_SETTINGS.keys()}
        if data != current_settings:
            try:
                for key in list(Config.DEFAULT_SETTINGS.keys())[:4]:
                    setattr(current_user, key.lower(), bool(int(request.form.get(key))))
                for key in list(Config.DEFAULT_SETTINGS.keys())[4:]:
                    setattr(current_user, key.lower(), int(request.form.get(key)))
            except ValueError:
                flash("settings updated unsuccessfully.")
                return redirect(url_for("main.settings"))
            else:
                db.session.commit()
                session["is_settings_changed"] = True
                flash("settings updated successfully.")
        else:
            flash("nothing have changed.")
        return redirect(url_for("main.settings"))
    if current_user.is_authenticated:
        data = {key: {
            "value": getattr(current_user, key.lower()),
            "title": item["title"],
            "description": item["description"],
        } for key, item in Config.DEFAULT_SETTINGS.items()}
    else:
        data = Config.DEFAULT_SETTINGS
    return render_template("views/settings.html", data=data)