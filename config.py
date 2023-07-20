
import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # dict[str, dict[str, bool|int]]
    DEFAULT_SETTINGS = {
        "NOTIFICATIONS_SYSTEM": {
            "value": True,
            "title": "system notifications",
            "description": "this controls whether you receive notifications or not. enabled by default. can technically be disabled, but the whole user experience would be ruined.",
        },
        "NOTIFICATIONS_TODOLIST": {
            "value": False,
            "title": "todolist notifications",
            "description": "enabled by literally no one.",
        },
        "NOTIFICATIONS_TIMER": {
            "value": False,
            "title": "neco-arc notifications",
            "description": "if enabled, we will tell you every time you complete a pomodoro session. disabled by default - even neco-arc hates it.",
        },
        "NOTIFICATIONS_CHATBOT": {
            "value": False,
            "title": "chatbot notifications",
            "description": "who on earth would enable this?",
        },
        "TIMER_WORK_SESSION_LENGTH": {
            "value": 45,
            "title": "work session",
            "description": "this controls the how long you will work per session. default is 45 minutes. feel free to opt differently however you like. it's ok, we won't judge you.",
        },
        "TIMER_SHORT_BREAK_SESSION_LENGTH": {
            "value": 5,
            "title": "short break session",
            "description": "you are smart, so we don't need to explain what this does.",
        },
        "TIMER_LONG_BREAK_SESSION_LENGTH": {
            "value": 15,
            "title": "long break session",
            "description": "devs are lazy so see above.",
        },
        "TIMER_INTERVAL": {
            "value": 4,
            "title": "interval",
            "description": "we can't yet explain this coherently. by default, the interval is 4, so on every 4th session, you will earn a long break instead of a short break. something like that.",
        },
    }

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

    # PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

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