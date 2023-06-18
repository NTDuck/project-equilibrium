
from flask import render_template, redirect, url_for, request, abort
from flask_login import login_user, logout_user, login_required

from . import auth
from .. import db
from ..models import User
from ..utils import UserDbHandler


userDbHandler = UserDbHandler(request, db)


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

        # check if email/username already exists
        if User.query.filter_by(email=email).first():
            # flash msg: email already in use
            abort(400)
        if User.query.filter_by(username=username).first():
            # flash msg: username already registered
            abort(400)
        # do something to validate form credentials, preferably regex

        # if everything is okay
        userDbHandler.create(email=email, username=username, password=password)
        userDbHandler.commit_session()
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")