
from flask import (
    flash, redirect, render_template, request, url_for, 
)
from flask_login import (
    current_user, login_required, login_user, logout_user, 
)
from werkzeug.security import safe_join

from .. import db
from ..models import User
from . import auth
from .forms import (
    LoginForm, RegistrationForm, 
)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if all((
            user is not None,
            user.verify_password(form.password.data),
        )):
            login_user(user=user, remember=form.remember_user.data)
            
            # redirect after successful login
            next_url = request.args.get("next_url")
            if any((
                next_url is None,
                not next_url.startswith("/"),
            )):
                next_url = safe_join(url_for("main.index"), next_url)
            return redirect(next_url)
        
        flash("Invalid email or password.")
    
    return render_template("auth/login.html", form=form)


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been signed out.")
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data.lower(),
            username=form.username.data,
            password=form.password.data,
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash("You have successfully registered.")
            return redirect(url_for("auth.login"))
        
        # handle exceptions
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}")
            return redirect(url_for("auth.register"))
    
    return render_template("auth/register.html", form=form)