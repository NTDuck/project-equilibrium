
from flask import render_template, redirect, url_for, request, abort
from flask_login import login_user, logout_user, login_required

from . import auth
from .. import userDbHandler
from ..models import User


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        
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
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        
        # validation
        validated_email = userDbHandler.validate_email(email)
        validated_username = userDbHandler.validate_username(username)
        validated_password = userDbHandler.validate_password(password)
        if any([i is None for i in [validated_email, validated_username, validated_password]]):
            abort(400)

        # if everything is okay
        userDbHandler.create(email=validated_email, username=validated_username, password=validated_password)
        userDbHandler.commit_session()
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")