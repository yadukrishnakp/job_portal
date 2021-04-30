from flask import Flask, render_template, redirect, url_for
from models import RegistrationForm, PostRegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'job portal'


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Job portal')


@app.route('/find_job', methods=['GET', 'POST'])
def find_job():
    return redirect(url_for('login'))


@app.route('/post_job_signup', methods=['GET', 'POST'])
def post_job_signup():
    form = PostRegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('post_job_signup'))
    return render_template('job_post_signup.html', title='Job portal', form=form)


@app.route('/post_job_signin', methods=['GET', 'POST'])
def post_job_signin():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('post_job_signin'))
    return render_template('job_post_signin.html', title='Job portal', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('register'))
    return render_template('register.html', title='Job portal', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('login'))
    return render_template('login.html', title='Job portal', form=form)


if __name__ == '__main__':
    app.run(debug=True)
