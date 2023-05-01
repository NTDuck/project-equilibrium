
from unittest import TestCase

from app import (
    create_app, db, 
)
from app.models import User


class UserModelTestCase(TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        user = User(password="dev")
        self.assertTrue(user.password_hash is not None)

    def test_no_password_getter(self):
        user = User(password="dev")
        with self.assertRaises(AttributeError):
            user.password

    def test_password_verification(self):
        user = User(password="dev")
        self.assertTrue(user.verify_password("dev"))
        self.assertFalse(user.verify_password("foo"))

    def test_password_salts_are_random(self):
        user_1 = User(password="dev")
        user_2 = User(password="foo")
        self.assertTrue(user_1.password_hash != user_2.password_hash)