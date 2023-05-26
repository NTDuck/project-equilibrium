
class Config:
    
    SECRET_KEY = "dev"

    TIMER_WORK_SESSION_LENGTH = 45
    TIMER_SHORT_BREAK_SESSION_LENGTH = 5
    TIMER_LONG_BREAK_SESSION_LENGTH = 15
    TIMER_INTERVAL = 4
    TIMER_DELAY = 1000   # miliseconds

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