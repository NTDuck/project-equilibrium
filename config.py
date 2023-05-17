
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    
    SECRET_KEY = "dev"

    # flask-moment
    MOMENT_USE_TZ = True

    # flask-htmlmin
    MINIFY_HTML = True

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