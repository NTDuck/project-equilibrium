
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg: Message):
    with app.app_context():
        mail.send(msg)

def send_email(recipients: list[str], subject: str, template: str, **kwargs) -> Thread:
    app = current_app._get_current_object()
    msg = Message(
        subject=subject,
        recipients=recipients,
        body=render_template(f"{template}.txt", **kwargs),
        html=render_template(f"{template}.html", **kwargs),
    )
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr