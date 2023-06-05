
class Config:
    SECRET_KEY = "dev"

    TIMER_WORK_SESSION_LENGTH = 45
    TIMER_SHORT_BREAK_SESSION_LENGTH = 5
    TIMER_LONG_BREAK_SESSION_LENGTH = 15
    TIMER_INTERVAL = 4
    TIMER_DELAY = 1000   # inevitable inaccuracy
    # timer delay affected by browser

    USER_DATA_ALLOWED_FILE_EXTENSIONS = {".json"}

    HUGGINGFACE_MODEL = "distilgpt2"
    HUGGINGFACE_MODEL_MIN_LENGTH = 20
    HUGGINGFACE_MODEL_MAX_LENGTH = 100

    # flask-sqlalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask-moment
    MOMENT_USE_TZ = True

    # flask-htmlmin
    MINIFY_HTML = True

    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///data-dev.db"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///data-test.db"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig,
}