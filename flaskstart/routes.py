
from flaskstart.models import User, Post #IMPORTANT TO PUT THIS IMPORT AFTER DEFINING db variable
from flask import Flask, render_template, url_for, flash, redirect
from flaskstart.forms import RegitrationForm, LoginForm
from flaskstart import app

postsByUsers = [
    {
        'author': 'Homer',
        'title': 'Strange Philosophy of Human Being',
        'content': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.",
        'date': 'June, 8th century BCE'
    },
    {
        'author': 'Aristotle',
        'title': 'Strange Philosophy of Homer Being',
        'content': "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.",
        'date': 'February, 	322 BC'
    }
]



@app.route("/") # декоратор, в цьому випадку реєструє маршрут на головну сторінку, після чого виконує клас/ф-цію знизу
@app.route("/home") # ще один декоратор, з іншим шляхом але веде на цю ж саму сторінку
def home():
    return render_template("home.html", postsRead=postsByUsers)


@app.route("/about") # ще один декоратор але з іншим шляхом, до сторінки про нас
def about():
    return render_template("about.html", title="Про Нас")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegitrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == '123':
            flash(f'You have been logged in by this email: {form.email.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed, check your Data!', 'danger')
    return render_template('login.html', title='Login', form=form)
