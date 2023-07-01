
from flask import render_template
from flask_login import current_user

from . import auth
from ..models import TimerSessionCount
from ..utils import current_streak, longest_streak


@auth.route("/profile")
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