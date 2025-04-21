# Форми
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # для картинки + обмеження по конкретним розширенням фото
from flask_login import current_user
from wtforms import TextAreaField
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
    
    
class SupportFrom(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=5, max=100)
    ])
    message = TextAreaField('Message', validators=[
        DataRequired()
    ])
    submit = SubmitField('Send')
    

class UpdateAccountForm(FlaskForm): 
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=2, max=20)
    ])
    
    email = StringField('Email',  validators=[
        DataRequired(),
        Email()
    ])
    
    picture = FileField('Update Profie Picture', validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Update')
    
    def validate_username(self, username): 
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user: 
                raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already in use. Please choose a different one.')
        
    