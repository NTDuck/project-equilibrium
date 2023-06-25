
import os
import click
from app import create_app, db


app = create_app(os.getenv("FLASK_CONFIG") or "default")


# note-to-self: never modify this
with app.app_context():
    db.create_all()


@app.cli.command()
@click.argument("test_names", nargs=-1)
def test(test_names):
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)