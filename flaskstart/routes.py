
import os # to grab file extention
import secrets # to randomly name uploaded pic
from PIL import Image # Pillow library
from flaskstart.models import User, Post, Support #IMPORTANT TO PUT THIS IMPORT AFTER DEFINING db variable
from flask import Flask, render_template, request, url_for, flash, redirect
from flaskstart.forms import RegitrationForm, LoginForm, SupportFrom, UpdateAccountForm
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

def save_picture_text(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
                #path to the package directory / pics static folder / name of pic
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)
    
    return picture_fn

@app.route("/") # декоратор, в цьому випадку реєструє маршрут на головну сторінку, після чого виконує клас/ф-цію знизу
@app.route("/home") # ще один декоратор, з іншим шляхом але веде на цю ж саму сторінку
def home():
    picturesRead = Support.query.all()
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture_text(form.picture.data)
            current_user.image_file = picture_file
    return render_template("home.html", postsRead=postsByUsers, picturesRead=picturesRead)


@app.route("/about") # ще один декоратор але з іншим шляхом, до сторінки про нас
def about():
    return render_template("about.html", title="Про Нас")


@app.route("/register", methods=['GET', 'POST']) # REGISTER ##########
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

@app.route("/login", methods=['GET', 'POST']) # LOGIN ##########
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





def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
                #path to the package directory / pics static folder / name of pic
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)
    
    return picture_fn #pic file name

@app.route("/account", methods=['GET', 'POST']) # UPDATE USER INFO ##########
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data 
        db.session.commit()
        flash(f'Your super cool account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET': # заповнити поля поточними даними
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', 
                           title='Account', 
                           image_file=image_file, 
                           form=form )

    
@app.route("/support", methods=['GET', 'POST'])
@login_required
def support():
    form = SupportFrom()
    if request.method == 'POST':
        if form.validate_on_submit():
            message = Support(title=form.title.data,
                              message=form.message.data,
                              user_id = current_user.id
                            )
            db.session.add(message)
            db.session.commit()
            flash(f'Your message has been successfully sent to the administrator!', 'success')
            return redirect(url_for('home'))
        else:
            print("*********** \n Form errors:", form.errors, "\n **********")
            flash(f'Fail to send your message! *_* ', 'danger')

    return render_template('support.html', title='Support', form=form)
    

@app.route("/admin_panel", methods=['GET', 'POST'])
@login_required
def admin_panel():
    messages = Support.query.all()
    return render_template('admin_panel.html', messageRead=messages, title="Admin Panel")
    

        