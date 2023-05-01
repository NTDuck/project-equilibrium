
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    
    SECRET_KEY = "dev"

    # bootstrap-flask configs
    BOOTSTRAP_SERVE_LOCAL = True

    # flask-sqlalchemy configs
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "instance", "data.sqlite")
    # SQLALCHEMY_ENGINE_OPTIONS = ...
    # SQLALCHEMY_BINDS = ...
    # SQLALCHEMY_ECHO = ...
    # SQLALCHEMY_RECORD_QUERIES = ...
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask-moment configs
    MOMENT_USE_TZ = True

    # app configs
    DEFAULT_GENERAL_CONFIG = {
        "theme": "dark", 
    }
    DEFAULT_POMODORO_CONFIG = {
        "work_minutes": 25,
        "short_break_minutes": 5,
        "long_break_minutes": 15,
        "pomodoros_until_long_break": 4,
    }
    DEFAULT_TASK_MANAGER_CONFIG = {
        "foo": "bar"
    }
    DEFAULT_MUSIC_PLAYER_CONFIG = {
        "foo": "bar"
    }
    DEFAULT_CHATBOT_CONFIG = {
        "foo": "bar"
    }

    def init_app(app):
        pass


class DevelopmentConfig(Config):

    DEBUG = True


class TestingConfig(Config):

    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig,
}