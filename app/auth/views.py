
from flask import render_template, redirect, url_for, request, abort
from flask_login import login_user, logout_user, login_required, current_user

from config import Config
from . import auth
from .. import db
from ..models import User
from ..email import send_email


@auth.before_app_request
def before_app_request():
    if current_user.is_authenticated:
        if all([
            not getattr(current_user, "confirmed"),
            request.blueprint != "auth",
            request.endpoint != "static",
        ]):
            return redirect(url_for("auth.unconfirmed"))
    

@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or getattr(current_user, "confirmed"):
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one()
        
        # will implement real things later, abort for now
        if user is None:
            # redirect to register page / flash msg
            return abort(400)
        if not user.verify_password(password):
            # false credentials
            return abort(400)

        # if everything is okay
        login_user(user)

        # will actually return the previous page user is in
        return redirect(url_for("main.index"))
    return render_template("auth/login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    # notify user via flash msg
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email").strip()
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        try:
            user = User(email=email, username=username, password=password)
        except ValueError:
            abort(400)
        else:
            db.session.add(user)
            db.session.commit()

        token = user.generate_confirmation_token()
        send_email([getattr(user, "email")], "confirm your account", "auth/email/confirm", user=user, token=token, expiration=f"{Config.CONFIRMATION_TOKEN_EXPIRATION // 60} minutes")

        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if getattr(current_user, "confirmed"):
        return redirect(url_for("main.index"))
    if current_user.validate_confirmation_token(token):
        setattr(current_user, "confirmed", True)
        db.session.commit()
        # flash msg
    else:
        ...
        # flash msg: token expired/invalid
    return redirect(url_for("main.index"))


@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email([getattr(current_user, "email")], "confirm your account", "auth/email/confirm", user=current_user, token=token, expiration=f"{Config.CONFIRMATION_TOKEN_EXPIRATION // 60} minutes")
    return redirect(url_for("main.index"))