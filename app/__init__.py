
from config import config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_htmlmin import HTMLMIN


db = SQLAlchemy()
migrate = Migrate()
htmlmin = HTMLMIN(remove_comments=True, remove_empty_space=True)
moment = Moment()


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    for ext in (
        db, htmlmin, moment,
    ):
        ext.init_app(app)
    migrate.init_app(app, db)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .api import api as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app