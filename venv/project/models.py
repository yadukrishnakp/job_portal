from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired(), Length(min=6, max=12)])
    confirm_password = StringField('Confirm password',
                                   validators=[DataRequired(), Length(min=6, max=12), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired(), Length(min=6, max=12)])
    submit = SubmitField('Login')


class PostRegistrationForm(FlaskForm):
    company_name = StringField('Company name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired(), Length(min=6, max=12)])
    confirm_password = StringField('Confirm password',
                                   validators=[DataRequired(), Length(min=6, max=12), EqualTo('password')])
    submit = SubmitField('Register')
