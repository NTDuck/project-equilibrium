
import os
import click
import secrets
from flask import session
from app import create_app, db
from app.models import Todolist


app = create_app(os.getenv("FLASK_CONFIG") or "default")


# note-to-self: never modify this
with app.app_context():
    db.create_all()


# @app.before_request
# def generate_csrf_token():
#     if "csrf_token" not in session:
#         session["csrf_token"] = secrets.token_hex(16)


@app.shell_context_processor
def shell_context_processor():
    return dict(db=db, TodolistItems=Todolist)


@app.cli.command()
@click.argument("test_names", nargs=-1)
def test(test_names):

    import unittest

    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)