
# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from flask_login import UserMixin, LoginManager, current_user, login_required, login_user
from flask_wtf import Form
from wtforms import StringField, SelectField, validators
from hashlib import md5


class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active






user_dict = {'austin': User('austin1','37b51d194a7513e45b56f6524f2d51f2'), 'admin':User('admin','37b51d194a7513e45b56f6524f2d51f2')}

USERS = {
    1: User(u"Austin", 1),
    2: User(u"Steve", 2),
    3: User(u"Ado", 3, ),
    4: User(u"Lord Hamilton", 4, ),
    5: User(u"Burt", 5, ),
    6: User(u"Robotobo", 6, ),
    7: User(u"Bubbs", 7, )
}

USER_NAMES = {u.name:u for u in USERS.values()}



# create the application object
app = Flask(__name__)

app.secret_key = "Flim flam"


# login_manager = LoginManager()
#
# login_manager.login_view = "login"
# login_manager.login_message = u"Please log in to access this page."



def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to log in to submit your pick')
            return redirect(url_for('login'))
    return wrap

# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    #return "Hello, World!"  # return a string
    return render_template('index.html')  # render a template

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


#class User()

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        pswd = md5(request.form['password'].encode('utf-8')).hexdigest()
        username = request.form['username']
        if username in USER_NAMES and pswd == '37b51d194a7513e45b56f6524f2d51f2':
            login_user(USER_NAMES[username])
            flash('You are now logged in as %s' %username)
            return render_template(url_for('submitpick'))
        else:
            error = "there was an error"
            flash('Sorry, but we could not log you in.')












        # if request.form['username'] not in user_dict.keys() or pswd != user_dict[str(request.form['username'])].password:
        #     error = 'Invalid Credentials. Please try again.'
        # else:
        #     session['logged_in'] = True
        #     user = request.form['username'].encode('utf-8')
        #     session['username'] = User[user].username
        #     flash('You are now logged in as %s.' % session['username'])
        #     return redirect(url_for('home'))
    return render_template('login.html', error=error)



@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('you are now logged out')
    return redirect(url_for('welcome'))



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
    app.run(debug=True)