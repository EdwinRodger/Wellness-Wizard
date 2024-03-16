import flask
import flask_login

app = flask.Flask(__name__)
app.secret_key = 'super secret string'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'root': {'password': 'root'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if flask.request.method == 'GET':
        return flask.render_template('signup.html')

    email = flask.request.form['email']
    if email in users:
        flask.flash('Email already exists!', 'danger')
        return flask.redirect(flask.url_for('signup'))
    
    if flask.request.form['password'] != flask.request.form['confirm_password']:
        flask.flash('Passwords do not match!', 'danger')
        return flask.redirect(flask.url_for('signup'))

    users[email] = {'password': flask.request.form['password']}
    return flask.redirect(flask.url_for('signin'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if flask.request.method == 'GET':
        return flask.render_template('signin.html')

    email = flask.request.form['email']
    if email in users and flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('dashboard'))

    flask.flash('Wrong username or password!', 'danger')
    return flask.redirect(flask.url_for('signin'))


@app.route('/dashboard')
@flask_login.login_required
def dashboard():
    return flask.render_template('dashboard.html')

@app.route('/aboutus')
@flask_login.login_required
def aboutus():
    return flask.render_template('AboutUs.html')

@app.route('/')
@app.route('/home')
def home():
    return flask.render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)