
from config import config

from flask import Flask
from flask_bootstrap import Bootstrap


exts = {
    "bootstrap": Bootstrap(),
}


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    for ext in exts.values():
        ext.init_app(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    return app