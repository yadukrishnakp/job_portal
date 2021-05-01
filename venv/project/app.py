from flask import Flask, render_template, redirect, url_for, flash
from models import RegistrationForm, PostRegistrationForm, LoginForm, PostJobVacancy, SearchJob, UpdateProfile
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'job portal'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# table creation#########################################
class User_advertiser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(15), unique=True, nullable=False)


class Job_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(20), nullable=False)
    job_description = db.Column(db.String(200), nullable=False)
    experience = db.Column(db.String(20), nullable=False)
    salary_range = db.Column(db.String(20), nullable=False)
    benefits = db.Column(db.String(150), nullable=False)
    apply_link = db.Column(db.String(40), nullable=False)


class User_seeker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)


class Update_Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(30), nullable=False)
    current_address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    district = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(30), nullable=False)
    university = db.Column(db.String(30), nullable=False)
    qualification = db.Column(db.String(30), nullable=False)


# home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Job portal')


# home page find job button
@app.route('/find_job', methods=['GET', 'POST'])
def find_job():
    return redirect(url_for('login'))


# register of job advertiser
@app.route('/post_job_signup', methods=['GET', 'POST'])
def post_job_signup():
    form = PostRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User_advertiser(company_name=form.company_name.data, username=form.username.data, email=form.email.data,
                               password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('post_job_signin'))
    return render_template('job_post_signup.html', title='Job portal', form=form)


# login of job advertiser
@app.route('/post_job_signin', methods=['GET', 'POST'])
def post_job_signin():
    form = LoginForm()
    form1 = PostJobVacancy()
    if form.validate_on_submit():
        user = User_advertiser.query.filter_by(email=form.email.data).first()
        if User_advertiser and bcrypt.check_password_hash(user.password, form.password.data):
            return render_template('login_advertiser.html', form=form1)
        else:
            flash('check email and password')
            return redirect(url_for('post_job_signin'))
    return render_template('job_post_signin.html', title='Job portal', form=form)


# after login job advertiser, post a job page
@app.route('/login_advertiser', methods=['GET', 'POST'])
def login_advertiser():
    form = PostJobVacancy()
    if form.validate_on_submit():
        return redirect(url_for('login_advertiser'))
    return render_template('login_advertiser.html', title='Job portal', form=form)


# register of job seeker
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User_seeker(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('register'))
    return render_template('register.html', title='Job portal', form=form)


# login of job seeker
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    form1 = SearchJob()
    if form.validate_on_submit():
        user = User_seeker.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            return render_template('job_seeker.html', form=form1)
        else:
            flash('check email and password')
            return redirect(url_for('login'))
    return render_template('login.html', title='Job portal', form=form)


# search job
@app.route('/job_seeker', methods=['GET', 'POST'])
def job_seeker():
    form = SearchJob()
    if form.validate_on_submit():
        return redirect(url_for('job_seeker'))
    return render_template('job_seeker.html', title='Job portal', form=form)


@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    form = UpdateProfile()
    if form.validate_on_submit():
        return redirect(url_for('update_profile'))
    return render_template('update_profile.html', title='Job portal', form=form)


if __name__ == '__main__':
    app.run(debug=True)
