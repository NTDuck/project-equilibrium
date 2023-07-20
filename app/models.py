
from datetime import datetime, date as d
import re

from flask_login import UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError
from jwt import decode, encode

from config import Config
from . import db, login_manager


class Base:
    __abstract__ = True

    @classmethod
    def validate(cls, value: str, attr, min_str_length=Config.USER_INPUT_MIN_STRING_LENGTH, max_str_length=Config.USER_INPUT_MAX_STRING_LENGTH, unique=True):
        return all([
            isinstance(value, str),
            min_str_length < len(value) < max_str_length,
            not value.isspace(),
            not unique or cls.query.filter_by(user=current_user, **{attr: value}).first() is None,
        ])
    
    """
    sqlalchemy.engine.row.Row -> db.Model
    only necessary if fetch() is used instead of scalars()
    """
    # @classmethod
    # def row_to_model(cls, r):
    #     if not isinstance(r, list):
    #         return r._asdict()[cls.__name__]
    #     return [cls.row_to_model(i) for i in r]


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _email = db.Column(db.String(256), unique=True, index=True)
    _username = db.Column(db.String(32), unique=True, index=True)
    password_hash = db.Column(db.String(256))

    # state
    confirmed = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.Date)

    # settings
    notifications_system = db.Column(db.Boolean, default=Config.DEFAULT_SETTINGS["NOTIFICATIONS_SYSTEM"])
    notifications_todolist = db.Column(db.Boolean, default=Config.DEFAULT_SETTINGS["NOTIFICATIONS_TODOLIST"])
    notifications_timer = db.Column(db.Boolean, default=Config.DEFAULT_SETTINGS["NOTIFICATIONS_TIMER"])
    notifications_chatbot = db.Column(db.Boolean, default=Config.DEFAULT_SETTINGS["NOTIFICATIONS_CHATBOT"])
    _timer_work_session_length = db.Column(db.Integer, default=Config.DEFAULT_SETTINGS["TIMER_WORK_SESSION_LENGTH"])
    _timer_short_break_session_length = db.Column(db.Integer, default=Config.DEFAULT_SETTINGS["TIMER_SHORT_BREAK_SESSION_LENGTH"])
    _timer_long_break_session_length = db.Column(db.Integer, default=Config.DEFAULT_SETTINGS["TIMER_LONG_BREAK_SESSION_LENGTH"])
    _timer_interval = db.Column(db.Integer, default=Config.DEFAULT_SETTINGS["TIMER_INTERVAL"])

    todolist = db.relationship("Todolist", backref="user", lazy=True)
    timer_session_count = db.relationship("TimerSessionCount", backref="user", 
    lazy=True)
    chatbot_message = db.relationship("ChatbotMessage", backref="user", lazy=True)

    @hybrid_property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email: str):
        if not all([
            0 < len(email) < 256,
            self.query.filter_by(email=email).first() is None,
        ]):
            raise ValueError
        try:
            validated_email = validate_email(email=email, check_deliverability=True)
            self._email = validated_email.normalized
        except (EmailNotValidError, EmailSyntaxError):
            raise ValueError
        
    @hybrid_property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, username: str):
        username = username.lower()
        if not all([
            re.match(pattern=Config.USER_USERNAME_REGEX_PATTERN, string=username) is not None,
            self.query.filter_by(username=username).first() is None,
        ]):
            raise ValueError
        self._username = username

    @property
    def password(self):
        raise AttributeError
    
    @password.setter
    def password(self, password: str):
        if re.match(pattern=Config.USER_PASSWORD_REGEX_PATTERN, string=password) is None:
            raise ValueError
        self.password_hash = generate_password_hash(password=password)
    
    def verify_password(self, password: str):
        return check_password_hash(self.password_hash, password=password)
    
    def generate_confirmation_token(self) -> str:
        return encode({
            "time": datetime.utcnow().isoformat(),
            "id": self.id,
        }, key=Config.SECRET_KEY, algorithm=Config.CONFIRMATION_TOKEN_ALGORITHM)

    def validate_confirmation_token(self, token: str, expiration=Config.CONFIRMATION_TOKEN_EXPIRATION) -> bool:
        # retrieve token
        try:
            credentials = decode(token, key=Config.SECRET_KEY, algorithms=Config.CONFIRMATION_TOKEN_ALGORITHM)
        except:
            return False

        # validate token
        if credentials.keys() != {"time", "id"}:
            return False
        
        time_generated = datetime.fromisoformat(credentials.get("time"))
        id = credentials.get("id")

        # check if token is expired
        time_now = datetime.utcnow()
        time_delta = time_now - time_generated
        if time_delta.seconds > expiration:
            return False
        
        return id == self.id
    
    def generate_password_reset_token(self) -> str:
        return encode({
            "time": datetime.utcnow().isoformat(),
            "id": self.id,
        }, key=Config.SECRET_KEY, algorithm=Config.CONFIRMATION_TOKEN_ALGORITHM)
    
    @classmethod
    def validate_password_reset_token(cls, token, expiration=Config.CONFIRMATION_TOKEN_EXPIRATION):   # return user if exists
        # retrieve token
        try:
            credentials = decode(token, key=Config.SECRET_KEY, algorithms=Config.CONFIRMATION_TOKEN_ALGORITHM)
        except:
            return False

        # validate token
        if credentials.keys() != {"time", "id"}:
            return False
        
        time_generated = datetime.fromisoformat(credentials.get("time"))
        id = credentials.get("id")

        # check if token is expired
        time_now = datetime.utcnow()
        time_delta = time_now - time_generated
        if time_delta.seconds > expiration:
            return False
        
        return db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
    
    # warning: violate DRY -> heresy
    @hybrid_property
    def timer_work_session_length(self):
        return self._timer_work_session_length
    
    @timer_work_session_length.setter
    def timer_work_session_length(self, value: int):
        if not all([
            isinstance(value, int),
            0 < value < 3600,
        ]):
            raise ValueError
        self._timer_work_session_length = value

    @hybrid_property
    def timer_short_break_session_length(self):
        return self._timer_short_break_session_length
    
    @timer_short_break_session_length.setter
    def timer_short_break_session_length(self, value: int):
        if not all([
            isinstance(value, int),
            0 < value < 3600,
        ]):
            raise ValueError
        self._timer_short_break_session_length = value

    @hybrid_property
    def timer_long_break_session_length(self):
        return self._timer_long_break_session_length
    
    @timer_long_break_session_length.setter
    def timer_long_break_session_length(self, value: int):
        if not all([
            isinstance(value, int),
            0 < value < 3600,
        ]):
            raise ValueError
        self._timer_long_break_session_length = value

    @hybrid_property
    def timer_interval(self):
        return self._timer_interval
    
    @timer_interval.setter
    def timer_interval(self, value: int):
        if not all([
            isinstance(value, int),
            0 < value < 99,
        ]):
            raise ValueError
        self._timer_interval = value


@login_manager.user_loader
def user_loader(user_id):
    return db.session.execute(db.select(User).where(User.id == int(user_id))).scalar_one()


class Todolist(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _value = db.Column(db.String(128), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    @hybrid_property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: str):
        if not super().validate(value=value, attr="value", unique=False):
            raise ValueError
        self._value = value


class TimerSessionCount(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _date = db.Column(db.Date, unique=True, nullable=False)
    _session_count = db.Column(db.SmallInteger, nullable=False, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    @hybrid_property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, date: d):
        if not isinstance(date, d):
            raise ValueError
        self._date = date
        
    @hybrid_property
    def session_count(self):
        return self._session_count
    
    @session_count.setter
    def session_count(self, session_count=1):
        if not all([
            isinstance(session_count, int),
            0 < session_count < 9999,   # 2-byte signed integer: [-32,768, 32,767]
        ]):
            raise ValueError
        self._session_count = session_count


class ChatbotMessage(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _value = db.Column(db.String(512), nullable=False)
    _type = db.Column(db.String(8), nullable=False, default="server")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    @hybrid_property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: str):
        if not super().validate(value=value, attr="value", max_str_length=512, unique=False):
            raise ValueError
        self._value = value

    @hybrid_property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type: str):
        if type not in {"server", "user"}:
            raise ValueError
        self._type = type