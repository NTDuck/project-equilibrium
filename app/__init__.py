
from config import config

from flask import Flask
from flask_moment import Moment
from flask_htmlmin import HTMLMIN

htmlmin = HTMLMIN(remove_comments=True, remove_empty_space=True)
moment = Moment()


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    for ext in (
        htmlmin, moment,
    ):
        ext.init_app(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app