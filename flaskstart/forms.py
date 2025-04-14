# Форми
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegitrationForm(FlaskForm):
    #validation of the form inside validators[]
    username = StringField('Username', validators=[ # перше значення це label, в другому додаю валідатори
        DataRequired(), 
        Length(min=2, max=20)
    ])
    
    email = StringField('Email',  validators=[
        DataRequired(),
        Email()
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    confirm_password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    
    submit = SubmitField('Sign Up')
    
    
class LoginForm(FlaskForm):
    email = StringField('Email',  validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    