from flask import Flask, render_template, redirect, url_for, flash, session
from models import RegistrationForm, PostRegistrationForm, LoginForm, PostJobVacancy, SearchJob, UpdateProfile, ApplyJob
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'job portal'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# t a b l e    c r e a t i o n    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class Job_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(30), nullable=False)
    job_title = db.Column(db.String(20), nullable=False)
    job_description = db.Column(db.String(200), nullable=False)
    key_qualification = db.Column(db.String(200), nullable=False)
    education = db.Column(db.String(35), nullable=False)
    experience = db.Column(db.String(20), nullable=False)
    salary_range = db.Column(db.String(20), nullable=False)
    benefits = db.Column(db.String(150), nullable=False)
    apply_link = db.Column(db.String(40), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    advertiser_company_name = db.Column(db.String(20))
    advertiser_username = db.Column(db.String(20))
    advertiser_email = db.Column(db.String(30), )
    advertiser_password = db.Column(db.String(15))
    seeker_email = db.Column(db.String(30), unique=True)
    seeker_password = db.Column(db.String(15))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Update_Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(30), nullable=False)
    current_address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    district = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(30), nullable=False)
    university = db.Column(db.String(30), nullable=False)
    qualification = db.Column(db.String(30), nullable=False)


class Applied_jobs(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(30), nullable=False)
    full_name = db.Column(db.String(30), nullable=False)
    current_address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    district = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
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
    rows = Job_details.query.all()
    f=0
    for r in rows:
        f+=1
    # row1 = Job_details.query.filter_by(id=f).first()
    # row2 = Job_details.query.filter_by(id=f - 1).first()
    # row3 = Job_details.query.filter_by(id=f - 2).first()
    list_row=[]
    for r in range(f, f-3, -1):
        row = Job_details.query.filter_by(id=r).first()
        list_row.append(row)
    return render_template('jobs_before_login.html', list_row=list_row)


# register of job advertiser
@app.route('/post_job_signup', methods=['GET', 'POST'])
def post_job_signup():
    form = PostRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(advertiser_company_name=form.company_name.data, advertiser_username=form.username.data,
                    advertiser_email=form.email.data, advertiser_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('account created, now login')
        return redirect(url_for('post_job_signup'))
    return render_template('job_post_signup.html', title='Job portal', form=form)


# login of job advertiser
@app.route('/post_job_signin', methods=['GET', 'POST'])
def post_job_signin():
    form = LoginForm()
    form1 = PostJobVacancy()
    if form.validate_on_submit():
        user = User.query.filter_by(advertiser_email=form.email.data).first()
        login_user(user)
        if User and bcrypt.check_password_hash(user.advertiser_password, form.password.data):
            return render_template('login_advertiser.html', form=form1)
        else:
            flash('check email and password')
            return redirect(url_for('post_job_signin'))
    return render_template('job_post_signin.html', title='Job portal', form=form)


# after login job advertiser and post a job page
@app.route('/login_advertiser', methods=['GET', 'POST'])
@login_required
def login_advertiser():
    form = PostJobVacancy()
    if form.validate_on_submit():
        user = Job_details(company_name=form.company_name.data, job_title=form.job_title.data,
                           job_description=form.job_description.data, key_qualification=form.key_qualification.data,
                           education=form.education.data,
                           experience=form.experience.data, salary_range=form.salary_range.data,
                           benefits=form.benefits.data, apply_link=form.apply_link.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_advertiser'))
    return render_template('login_advertiser.html', title='Job portal', form=form)


# register of job seeker
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(seeker_email=form.email.data, seeker_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('account created')
        return redirect(url_for('register'))
    return render_template('register.html', title='Job portal', form=form)


# login of job seeker
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    form1 = SearchJob()
    if form.validate_on_submit():
        user1 = Job_details.query.all()
        user = User.query.filter_by(seeker_email=form.email.data).first()
        login_user(user)
        if user and bcrypt.check_password_hash(user.seeker_password, form.password.data):
            return render_template('job_seeker.html', form=form1, user=user1)
        else:
            flash('check email and password')
            return redirect(url_for('login'))
    return render_template('login.html', title='Job portal', form=form)


# search job
@app.route('/job_seeker', methods=['GET', 'POST'])
@login_required
def job_seeker():
    user1 = Job_details.query.all()
    form = SearchJob()
    if form.validate_on_submit():
        return redirect(url_for('job_seeker'))
    return render_template('job_seeker.html', title='Job portal', form=form, user=user1)


@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfile()
    user1 = Update_Profile.query.filter_by(email=current_user.seeker_email).first()
    if user1:
        form.full_name.data = user1.full_name
        form.current_address.data = user1.current_address
        form.city.data = user1.city
        form.district.data = user1.district
        form.state.data = user1.state
        form.pin_code.data = user1.pin_code
        form.email.data = user1.email
        form.phone_number.data = user1.phone_number
        form.position.data = user1.position
        form.university.data = user1.university
        form.qualification.data = user1.qualification
    if form.validate_on_submit():
        user = Update_Profile(full_name=form.full_name.data, current_address=form.current_address.data,
                              city=form.city.data, district=form.district.data, state=form.state.data,
                              pin_code=form.pin_code.data,
                              email=form.email.data, phone_number=form.phone_number.data, position=form.position.data,
                              university=form.university.data, qualification=form.qualification.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('update_profile'))
    return render_template('update_profile.html', title='Job portal', form=form)


@app.route('/apply_jobs', methods=['GET', 'POST'])
@login_required
def apply_jobs():
    form = ApplyJob()
    user1 = Update_Profile.query.filter_by(email=current_user.seeker_email).first()
    if user1:
        form.full_name.data = user1.full_name
        form.current_address.data = user1.current_address
        form.city.data = user1.city
        form.district.data = user1.district
        form.state.data = user1.state
        form.pin_code.data = user1.pin_code
        form.email.data = user1.email
        form.phone_number.data = user1.phone_number
        form.position.data = user1.position
        form.university.data = user1.university
        form.qualification.data = user1.qualification
    if form.validate_on_submit():
        check_user = Job_details.query.filter_by(company_name=form.company_name.data).first()
        if check_user:
            user = Applied_jobs(company_name=form.company_name.data, full_name=form.full_name.data,
                                current_address=form.current_address.data,
                                city=form.city.data, district=form.district.data, state=form.state.data,
                                pin_code=form.pin_code.data,
                                email=form.email.data, phone_number=form.phone_number.data, position=form.position.data,
                                university=form.university.data, qualification=form.qualification.data)
            db.session.add(user)
            db.session.commit()
            flash('applied successfully')
            return redirect(url_for('apply_jobs'))
        else:
            flash('check company name same as advertisement')
            return redirect(url_for('apply_jobs'))
    return render_template('apply_jobs.html', title='Job portal', form=form)


@app.route('/applied_job_seeker', methods=['GET', 'POST'])
@login_required
def applied_job_seeker():
    user = Applied_jobs.query.filter_by(email=current_user.seeker_email)
    if user:
        return render_template('applied_jobs.html', user=user)


@app.route('/show_applicants', methods=['GET', 'POST'])
@login_required
def show_applicants():
    user = Applied_jobs.query.filter_by(company_name=current_user.advertiser_company_name)
    return render_template('show_applied_jobs.html', user=user)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    result_list = []
    form = SearchJob()
    search_result = form.search.data
    user = Job_details.query.all()
    if form.validate_on_submit():
        if search_result:
            for u in user:
                if search_result in u.experience:
                    result_list = Job_details.query.filter_by(experience=search_result)
                    return render_template('show_search_result.html', result=result_list)
                elif search_result in u.company_name:
                    result_list = Job_details.query.filter_by(company_name=u.company_name)
                    return render_template('show_search_result.html', result=result_list)
                elif search_result in u.job_title:
                    result_list = Job_details.query.filter_by(job_title=u.job_title)
                    return render_template('show_search_result.html', result=result_list)
                elif search_result in u.education:
                    results = Job_details.query.filter_by(education=u.education)
                    for result in results:
                        result_list.append(result)
                elif search_result in u.key_qualification:
                    results = Job_details.query.filter_by(key_qualification=u.key_qualification)
                    for result in results:
                        result_list.append(result)
            return render_template('show_search_result.html', result=result_list)
    return redirect(url_for('job_seeker'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/logoutt', methods=['GET', 'POST'])
@login_required
def logoutt():
    logout_user()
    session.pop('userr', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
