
from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_htmlmin import HTMLMIN

from config import config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
htmlmin = HTMLMIN(remove_comments=True, remove_empty_space=True)
moment = Moment()

login_manager.login_view = "auth.login"

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth.login"))


# placed here to avoid circular dependency
from .utils import UserDbHandler, TodolistDbHandler, TimerSessionCountDbHandler, ChatbotMessageDbHandler

userDbHandler = UserDbHandler(request, db)
todolistDbHandler = TodolistDbHandler(request, db)
timerSessionCountDbHandler = TimerSessionCountDbHandler(request, db)
chatbotMessageDbHandler = ChatbotMessageDbHandler(request, db)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    for ext in (
        db, htmlmin, login_manager, moment,
    ):
        ext.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from .api import api as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app