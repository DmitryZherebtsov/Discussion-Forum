# Форми
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flaskstart.models import User

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
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user: # Якщо користувача ще не має, перевірка не підніметься. Якщо є - тоді так і отримаємо помилку
            raise ValidationError('That username is taken. Please choose different one.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose different one.')
        

    
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
    
    