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
        return "Great", score, subject

    elif(score >= 71 and score <= 85):
        return "Good", score, subject

    elif(score >= 50 and score <= 70):
        return "Okay", score, subject

    elif(score >= 35 and score <= 49):
        return "Bad", score, subject

    elif(score >= 20 and score <= 34):
        return "Worst", score, subject

    else:
        return "Dead", score, subject
    
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
    suggestion = ""
    result, points, subject = score(points, subject)
    if subject.lower() == "depression":
        if result == "Great":
            suggestion = "You are a happy person!"
        elif result == "Good":
            suggestion = "Probably Depressed ! No need to worry."
        elif result == "Okay":
            suggestion = "lifestyle modification: Lifestyle changes such as regular exercise, healthy eating, adequate sleep, stress management, social support, limiting alcohol and substance use, setting realistic goals, engaging in enjoyable activities.These changes can improve mood, reduce symptoms, and contribute to overall well-being."
        elif result == "Bad":
            suggestion = "Psychological therapies like Cognitive Behavioral Therapy (CBT) and Interpersonal Therapy (IPT), whether provided by a mental health professional or through online platforms, can effectively treat depression by addressing negative thought patterns, improving interpersonal relationships, and teaching coping skills."
        elif result == "Worst":
            suggestion = "Medical treatments for depression include antidepressant medications, electroconvulsive therapy (ECT), transcranial magnetic stimulation (TMS), ketamine therapy, and lifestyle modifications. "
        elif result == "Dead":
            suggestion = "Seek Professional Help: If you're experiencing severe depression, it's crucial to reach out to a qualified mental health professional, such as a psychiatrist, psychologist, or counselor, for an accurate diagnosis and treatment plan."

    if subject.lower() == "anxiety":
        if result == "Great":
            suggestion = "You are a happy person!"
        elif result == "Good":
            suggestion = "Mild Anxiety ! No need to worry."
        elif result == "Okay":
            suggestion = "Moderate Anxiety ! Cognitive Behavioral Therapy (CBT): CBT helps individuals recognize and challenge irrational thoughts and beliefs contributing to anxiety.It teaches coping skills such as relaxation techniques, problem-solving, and exposure therapy."
        elif result == "Bad":
            suggestion = "Severe Anxiety ! Cognitive Behavioral Therapy (CBT) with Exposure and Response Prevention (ERP) and medication"
        elif result == "Worst":
            suggestion = "Panic Attacks or Panic Disorder ! Exposure Therapy and Gradual exposure to panic-inducing situations or sensations can help individuals become less sensitive to triggers over time.and Medication"
        elif result == "Dead":
            suggestion = "chronic or Treatment-Resistant Anxiety ! Seek Professional Help: If you're experiencing severe Anxiety, it's crucial to reach out to a qualified mental health professional, such as a psychiatrist, psychologist, or counselor, for an accurate diagnosis and treatment plan."
    
    if subject.lower() == "internet addiction":
        if result == "Great":
            suggestion = "You are a happy person!"
        elif result == "Good":
            suggestion = "Mild Addiction ! No need to worry. Psychoeducation: Educate the individual about internet addiction, its symptoms, and potential consequences , Self-monitoring: Encourage the individual to track their internet usage and identify triggers."
        elif result == "Okay":
            suggestion = "Moderate Addiction ! Individual therapy: Conduct one-on-one therapy sessions to address underlying psychological issues contributing to addiction , Stress management techniques: Teach relaxation techniques such as mindfulness meditation or deep breathing exercises to manage stress without relying on the internet."
        elif result == "Bad":
            suggestion = "Moderate to Severe Addiction ! Individual therapy addresses underlying psychological issues, Stress management techniques like meditation help manage stress.Inpatient treatment offers intensive therapy and monitoring may also help."
        elif result == "Worst":
            suggestion = "Severe Addiction ! Inpatient treatment: Consider inpatient or residential treatment programs for intensive therapy and monitoring , Detoxification if necessary: Address any physical dependence or withdrawal symptoms that may arise from excessive internet use , Pharmacotherapy: Consider medication to manage co-occurring mental health conditions such as depression or anxiety."
        elif result == "Dead":
            suggestion = "Chronic Addiction ! Long-term therapy: Engage in ongoing therapy to address deep-seated issues and maintain progress , Relapse prevention: Develop a comprehensive relapse prevention plan that includes identifying triggers, coping strategies, and support networks."

    print(suggestion)
    return flask.render_template('result.html', subject=subject, points=points, suggestion=suggestion, result=result)


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