# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import (LoginManager, login_required,
                            login_user, logout_user, UserMixin, current_user
                            )

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active


USERS = {
    1: User(u"Me", 1),
    2: User(u"Steve", 2),
}

USER_NAMES = dict((u.name, u) for u in USERS.values())


app = Flask(__name__)

SECRET_KEY = "Everyone knows this"
DEBUG = True

app.config.from_object(__name__)

login_manager = LoginManager()


@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))

login_manager.init_app(app)

@app.route("/")
@login_required
def index():
    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        if username in USER_NAMES:
            if login_user(USER_NAMES[username]):
                flash("Logged in as %s!" %current_user.name)
                print(current_user)
                return redirect(url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("login.html")



@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run()