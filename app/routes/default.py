from flask import render_template, redirect, url_for
from app import app
from flask_login import login_required, logout_user
from datetime import timedelta, date
import requests
from app.models import Session, Event


@app.route("/")
@login_required
def main():
    mock = {}
    for item in range(1, 6):
        events = [requests.get(f"https://rickandmortyapi.com/api/character/{item}")]
        event_date = date.today() + timedelta(days=item)
        date_str = event_date.strftime("%d %B")
        mock[date_str] = [event.json().get("name") for event in events]

        session = Session()
        event1 = Event()
        event1.date = event_date
        event1.header = events[0].json().get("name")
        event1.describe = events[0].json().get("name")
        session.add(event1)
        session.commit()
    return render_template('main.html', iterable=mock)


@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
