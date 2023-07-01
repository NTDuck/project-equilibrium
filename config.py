
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    TODOLIST_EXAMPLE_MESSAGES = [
        "hello, dear user!",
        "this is a simple todolist.",
        "you can add, edit, or delete items however you like!",
        "oh, please also play with the neco-arc in the middle.",
    ]
    CHATBOT_EXAMPLE_MESSAGES = [
        "this is an AI-powered chatbot! you can type in some text,",
        "and the server will respond with something. just don't expect much.",
    ]

    TIMER_WORK_SESSION_LENGTH = 45
    TIMER_SHORT_BREAK_SESSION_LENGTH = 5
    TIMER_LONG_BREAK_SESSION_LENGTH = 15
    TIMER_INTERVAL = 4
    TIMER_DELAY = 1000   # inevitable inaccuracy
    # timer delay affected by browser

    USER_INPUT_MIN_STRING_LENGTH = 0
    USER_INPUT_MAX_STRING_LENGTH = 128

    """
    username regex:
    from 8 to 32 characters
    contains lowercase letters, numbers, and underscores only
    consecutive underscores are not allowed
    numbers or underscores are not allowed at the beginning
    underscores are not allowed at the end
    """
    USER_USERNAME_REGEX_PATTERN = r"^(?![_\d])[a-z\d_]+(?<!_){8,32}$"
    """
    password regex:
    from 8 to 32 characters
    contains at least 1 uppercase letter, 1 lowercase letter, 1 number, 1 special character
    """
    USER_PASSWORD_REGEX_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%^&*<>?])[A-Za-z\d@~!@#$%^&*<>?]{8,32}$"

    CONFIRMATION_TOKEN_ALGORITHM = "HS256"
    CONFIRMATION_TOKEN_EXPIRATION = 3600   # seconds

    USER_DATA_ALLOWED_FILE_EXTENSIONS = {".json"}

    """
    uses Gmail SMTP server: https://support.google.com/a/answer/176600
    implement daily mail count to avoid being locked out of account
    """
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))   # uses 
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = "project-equilibrium@gmail.com"

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