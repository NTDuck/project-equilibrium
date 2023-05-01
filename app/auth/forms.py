
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, PasswordField, StringField, SubmitField, ValidationError, 
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, Regexp, 
)

from ..models import User


class LoginForm(FlaskForm):

    email = StringField(label="Email", validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField(label="Password", validators=[DataRequired()])
    
    remember_user = BooleanField(label="Keep me logged in")
    submit = SubmitField(label="Log in")


class RegistrationForm(FlaskForm):

    email = StringField(label="Email", validators=[DataRequired(), Email(), Length(1, 64)])
    username = StringField(
        label="Username",
        validators=[
            DataRequired(),
            Length(4, 64),
            Regexp(
                regex=r"^(?!_)(?!.*?_$)[a-zA-Z0-9_]{4,64}$",
                flags=0,
                message="Invalid username. Must be 4-64 characters, alphanumeric characters and underscores only. Underscores not allowed at beginning or end."
            )
        ]
    )
    password = PasswordField(
        label="Password",
        validators=[
            DataRequired(),
            Length(8, 64),
            Regexp(
                regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[A-Za-z0-9]{8,32}$",
                flags=0,
                message="Invalid password. Must be 8-32 characters, alphanumeric characters only. Must contain at least one uppercase letter, one lowercase letter and one number."
            ),
            EqualTo(
                fieldname="password_confirm",
                message="Passwords do not match."
            )
        ]
    )
    password_confirm = PasswordField(label="Confirm password", validators=[DataRequired()])
    
    submit = SubmitField(label="Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")
        
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already registered.")