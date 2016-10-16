
from flask_wtf import Form
from wtforms import StringField, SelectField, validators
from flask import Flask, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user, login_required
from oauth import OAuthSignIn


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '1194113453996121',
        'secret': '08790eb0f7a9f25a63d3398cb0c05bf0'
    },
    'twitter': {
        'id': '3RzWQclolxWZIMq5LJqzRZPTl',
        'secret': 'm9TEd58DSEtRrZHpz2EjrV9AhsBRxKMo8m3kuIZj3zLwzwIimt'
    }
}

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


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






# start the server with the 'run()' method
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)