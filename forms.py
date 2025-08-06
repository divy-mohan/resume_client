from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FloatField, BooleanField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    service = SelectField('Service Interested In', choices=[
        ('resume-writing', 'Resume Writing'),
        ('linkedin-profile', 'LinkedIn Profile Optimization'),
        ('cover-letter', 'Cover Letter Writing'),
        ('sop-lor', 'SOP/LOR Writing'),
        ('career-counselling', 'Career Counselling'),
        ('other', 'Other')
    ])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])

class OrderForm(FlaskForm):
    package_id = IntegerField('Package', validators=[DataRequired()])
    current_resume = FileField('Upload Current Resume', validators=[
        FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and Word documents allowed!')
    ])
    notes = TextAreaField('Additional Requirements', validators=[Optional(), Length(max=1000)])

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class NewsletterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])

class BlogCommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=10, max=1000)])

class ChatMessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=1000)])
