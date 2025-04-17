
from flaskstart.models import User, Post #IMPORTANT TO PUT THIS IMPORT AFTER DEFINING db variable
from flask import Flask, render_template, request, url_for, flash, redirect
from flaskstart.forms import RegitrationForm, LoginForm
from flaskstart import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegitrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You can login now by the name: {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # беру першого юзера по мейлу який він ввів
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
                                    #  if next_page not none
        else:
            flash('Login Failed, check your email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
    # if current_user.is_authenticated:
    #     return render_template('account.html', title='Account')
    # else:
    #     return redirect(url_for('login'))
    