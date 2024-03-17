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

def score(score, subject):
    if subject != "Depression":
        score *= 2
    if(score >= 86):
        return "Great"

    elif(score >= 71 and score <= 85):
        return "Good"

    elif(score >= 50 and score <= 70):
        return "Okay"

    elif(score >= 35 and score <= 49):
        return "Bad"

    elif(score >= 20 and score <= 34):
        return "Worst"

    else:
        return "Dead"
    
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

@app.route('/result/<subject>/<int:points>')
def result(subject, points):
    return flask.render_template('result.html', subject=subject, result=points)

@app.route('/sign_out')
def sign_out():
    flask_login.logout_user()
    flask.flash('You have been logged out!', 'success')
    return flask.redirect(flask.url_for('home'))


@app.route('/test/<subject>/<int:qno>', methods=['GET', 'POST'])
@flask_login.login_required
def test(subject, qno):
    if flask.request.method == 'POST':
        if 'score' not in flask.session:
            flask.session['score'] = 0 
        option = flask.request.form.getlist("options")
        if flask.request.method == 'POST':
            option = flask.request.form.getlist("options")
            if "option1" in option:
                flask.session['score'] += 1
            elif "option2" in option:
                flask.session['score'] += 2
            elif "option3" in option:
                flask.session['score'] += 3
            elif "option4" in option:
                flask.session['score'] += 4
            elif "option5" in option:
                flask.session['score'] += 5
            else:
                pass
            return flask.redirect(flask.url_for('test', subject=subject, qno=qno+1))
    
    if qno == 0:
        flask.session['score'] = 0

    if subject == "Depression":
        with open("src\\questions\\Depression.csv", "r") as f:
            QA = f.readlines()
    if subject == "Anxiety":
        with open("src\\questions\\Anxiety.csv", "r") as f:
            QA = f.readlines()
    if subject == "Addiction":
        with open("src\\questions\\Addiction.csv", "r") as f:
            QA = f.readlines()
    try:
        que = QA[qno].split(",")[0]
        ans = QA[qno].split(",")[1:]
    except:
        return flask.redirect(flask.url_for('result', points=flask.session['score'], subject=subject))
    return flask.render_template('test.html', subject=subject, que=que, ans=ans)

@app.route('/dashboard')
def dashboard():
    return flask.render_template('dashboard.html')

@app.route('/aboutus')
def aboutus():
    return flask.render_template('AboutUs.html')

@app.route('/')
@app.route('/home')
def home():
    return flask.render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)