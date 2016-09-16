# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, LoginManager, current_user, login_required, login_user, logout_user
from flask_wtf import Form
from wtforms import StringField, SelectField, validators
from hashlib import md5
from flaskext.zodb import ZOBDB



class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active



USERS = {
    1: User(u"Austin", 1),
    2: User(u"Steve", 2),
    3: User(u"Ado", 3, ),
    4: User(u"Lord Hamilton", 4, ),
    5: User(u"Burt", 5, ),
    6: User(u"Robotobo", 6, ),
    7: User(u"Bubbs", 7, )
}

USER_NAMES = dict((u.name, u) for u in USERS.values())


app = Flask(__name__)

SECRET_KEY = "Everyone knows this"
DEBUG = True

db = ZOBDB(app)

app.config.from_object(__name__)
app.config['ZODB_STORAGE'] = 'file://app.fs'
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
                return redirect(url_for("submitpick"))
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


class PickForm(Form):
    remaining_teams = [
        ('Bears', 'Bears'),
        ('Bengals',  'Bengals'),
        ('Bills', 'Bills'),
        ('Broncos', 'Broncos'),
        ('Browns' ,'Browns' ),
        ('Bucaneers', 'Bucaneers'),
        ('Cardinals' ,'Cardinals' ),
        ('Chargers' ,'Chargers'),
        ('Chiefs' ,'Chiefs' ),
        ('Colts'  ,'Colts' ),
        ('Cowboys', 'Cowboys' ),
        ('Dolphins', 'Dolphins' ),
        ('Eagles'  ,'Eagles' ),
        ('Falcons' ,'Falcons' ),
        ('Giants'  ,'Giants' ),
        ('Jaguars' ,'Jaguars' ),
        ('Jets', 'Jets' ),
        ('Lions', 'Lions' ),
        ('Packers', 'Packers'),
        ('Panthers', 'Panthers'),
        ('Patriots' ,'Patriots' ),
        ('Raiders', 'Raiders'),
        ('Rams' , 'Rams' ),
        ('Ravens', 'Ravens'),
        ('Redskins', 'Redskins'),
        ('Saints' , 'Saints' ),
        ('Seahawks', 'Seahawks' ),
        ('Steelers' , 'Steelers' ),
        ('Texans', 'Texans' ),
        ('Titans' ,'Titans' ),
        ('Vikings' ,'Vikings')
    ]
    MyField = SelectField('Make your pick:', choices = remaining_teams, validators = [validators.DataRequired()])




@app.route('/submitpick', methods= ['GET', 'POST'])
@login_required
def submitpick():
    form = PickForm()
    if form.validate_on_submit():
        flash('thanks for the pick')

    return render_template('submitpick.html', form = form)










if __name__ == "__main__":
    app.run()