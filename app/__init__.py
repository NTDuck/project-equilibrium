
import os

from config import config

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
migrate = Migrate()
moment = Moment()
db = SQLAlchemy()

login_manager.login_view = "auth.login"


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    for ext in (
        login_manager, moment, db,  
    ):
        ext.init_app(app)
    migrate.init_app(app, db)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app