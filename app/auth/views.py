
from datetime import date
from flask import render_template, redirect, url_for, request, session, abort, flash
from flask_login import login_user, logout_user, login_required, current_user

from config import Config
from . import auth
from .. import db
from ..models import User, TimerSessionCount
from ..utils import current_streak, longest_streak
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
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
        if user is None:
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                flash("user does not exist, please register instead.")
            return redirect(url_for("auth.register"))
        if not user.verify_password(password):
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                flash("false credentials.")
            return redirect(url_for("auth.login"))
        # if everything is okay
        login_user(user)
        if session["settings"]["NOTIFICATIONS_SYSTEM"]:
            flash("logged in successfully.")
        return redirect(url_for("main.index"))
    return render_template("auth/login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    if session["settings"]["NOTIFICATIONS_SYSTEM"]:
        flash("logged out successfully.")
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email").strip()
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        try:
            user = User(email=email, username=username, password=password, date_joined=date.today())
        except ValueError:
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                flash("registered unsuccessfully. please try again.")
            return redirect(url_for("auth.register"))
        else:
            db.session.add(user)
            db.session.commit()
        token = user.generate_confirmation_token()
        send_email([getattr(user, "email")], "confirm your account", "auth/email/confirm", user=user, token=token, expiration=f"{Config.CONFIRMATION_TOKEN_EXPIRATION // 60} minutes")
        if session["settings"]["NOTIFICATIONS_SYSTEM"]:
            flash("registered successfully.")
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
        if session["settings"]["NOTIFICATIONS_SYSTEM"]:
            flash("token confirmed successfully.")
    else:
        if session["settings"]["NOTIFICATIONS_SYSTEM"]:
            flash("token invalid. please try again.")
    return redirect(url_for("main.index"))


@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email([getattr(current_user, "email")], "confirm your account", "auth/email/confirm", user=current_user, token=token, expiration=f"{Config.CONFIRMATION_TOKEN_EXPIRATION // 60} minutes")
    return redirect(url_for("main.index"))


@auth.route("/profile")
@login_required
def profile():
    timer_data = getattr(current_user, TimerSessionCount.__tablename__)
    session_counts = [getattr(i, "session_count") for i in timer_data] if timer_data else []
    data = {
        "username": getattr(current_user, "username"),
        "date_joined": getattr(current_user, "date_joined").strftime("joined %b %d %Y"),
        "current_streak": current_streak(session_counts),
        "longest_streak": longest_streak(session_counts),
        "pomodoro_completed": sum(session_counts),
        "max_session_count": max(session_counts) if timer_data else 1,
        "session_count_chart_data": [[item.date.strftime("%b"), item.date.strftime("%d"), item.session_count] for item in timer_data],
    }
    return render_template("auth/profile.html", data=data)


@auth.route("/password/update", methods=["GET", "POST"])
@login_required
def password_update():
    if request.method == "POST":
        old_password = request.form.get("old-password").strip()
        new_password = request.form.get("new-password").strip()
        if not current_user.verify_password(old_password):
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                flash("old password not match")
            return redirect(url_for("auth.password_update"))
        try:
            setattr(current_user, "password", new_password)
        except ValueError:
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                flash("password invalid. please try again.")
            return redirect(url_for("auth.password_update"))
        else:
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                flash("password updated successfully.")
            db.session.commit()
        return redirect(url_for("auth.profile"))
    return render_template("auth/password-update.html")


@auth.route("/password/reset", methods=["GET", "POST"])
def password_reset_request():
    if request.method == "POST":
        email = request.form.get("email").strip()
        try:
            user = db.session.execute(db.select(User).where(User.email == email)).scalar_one()
        except:
            return abort(400)   # ?
        if user is None:
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                flash("user does not exist, please register instead.")
            return redirect(url_for("auth.register"))
        token = user.generate_password_reset_token()
        send_email([getattr(user, "email")], "password reset", "auth/email/password-reset", user=user, token=token, expiration=f"{Config.CONFIRMATION_TOKEN_EXPIRATION // 60} minutes")
        return render_template("auth/password-reset-pending.html", user=user)
    return render_template("auth/password-reset-request.html")


@auth.route("/password/reset/<token>", methods=["GET", "POST"])
def password_reset_confirm(token):
    if request.method == "POST":
        new_password = request.form.get("password").strip()
        user = User.validate_password_reset_token(token=token)
        if not user:
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                flash("token invalid. please try again.")
            abort(400)
        try:
            setattr(user, "password", new_password)
        except ValueError:
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                flash("password invalid. please try again.")
            abort(400)
        else:
            db.session.commit()
            session.pop("password_reset_token", None)   # remove from session if exists
            if session["settings"]["NOTIFICATIONS_SYSTEM"]:
                flash("password reset successfully.")
            return redirect(url_for("auth.login"))
    session["password_reset_token"] = token   # store to session
    return render_template("auth/password-reset.html", token=token)