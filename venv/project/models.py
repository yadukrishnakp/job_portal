from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=15)])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), Length(min=6, max=12), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=15)])
    submit = SubmitField('Login')


class PostRegistrationForm(FlaskForm):
    company_name = StringField('Company name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=15)])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), Length(min=6, max=15), EqualTo('password')])
    submit = SubmitField('Register')


class PostJobVacancy(FlaskForm):
    company_name = StringField('Company name', validators=[DataRequired()])
    job_title = StringField('Job title', validators=[DataRequired()])
    job_description = TextAreaField('Job description', validators=[DataRequired()])
    key_qualification = TextAreaField('Key qualification', validators=[DataRequired()])
    education= StringField('Education', validators=[DataRequired()])
    experience = StringField('Job experience', validators=[DataRequired()])
    salary_range = IntegerField('Salary range', validators=[DataRequired()])
    benefits = TextAreaField('Benefits', validators=[DataRequired()])
    apply_link = StringField('Apply link', validators=[DataRequired()])
    submit = SubmitField('Post')


class SearchJob(FlaskForm):
    search = StringField('search',  validators=[DataRequired()], render_kw={"placeholder": "title, skill, company, experience, qualification, state"})
    submit = SubmitField('Search')


class UpdateProfile(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    current_address = TextAreaField('Current Address', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    district = StringField('District', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    pin_code = IntegerField('Pincode', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    position = StringField('Position you are applying for', validators=[DataRequired()])
    university = StringField('University', validators=[DataRequired()])
    qualification = StringField('Highest Qualification', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ApplyJob(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    current_address = TextAreaField('Current Address', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    district = StringField('District', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    pin_code = IntegerField('Pincode', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    position = StringField('Position you are applying for', validators=[DataRequired()])
    university = StringField('University', validators=[DataRequired()])
    qualification = StringField('Highest Qualification', validators=[DataRequired()])
    submit = SubmitField('Submit')
