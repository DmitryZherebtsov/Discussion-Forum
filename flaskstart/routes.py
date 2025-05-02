
import os # to grab file extention
import secrets # to randomly name uploaded pic
from PIL import Image # Pillow library
from flaskstart.models import User, Post, Support # IMPORTANT TO PUT THIS IMPORT AFTER DEFINING db variable
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from flaskstart.forms import (RegitrationForm, LoginForm, SupportFrom, UpdateAccountForm, 
                              PostForm, RequestResetForm, ResetPasswordForm)
from flaskstart import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

# postsByUsers = [ # test posts as Dummy data
#     {
#         'author': 'Homer',
#         'title': 'Strange Philosophy of Human Being',
#         'content': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.",
#         'date': 'June, 8th century BCE'
#     },
#     {
#         'author': 'Aristotle',
#         'title': 'Strange Philosophy of Homer Being',
#         'content': "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.",
#         'date': 'February, 	322 BC'
#     }
# ]

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


########## MAIN PAGE ##########
@app.route("/") # декоратор, в цьому випадку реєструє маршрут на головну сторінку, після чого виконує клас/ф-цію знизу
@app.route("/home") # ще один декоратор, з іншим шляхом але веде на цю ж саму сторінку
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    
    picturesRead = Support.query.all()
    form = UpdateAccountForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture_text(form.picture.data)
            current_user.image_file = picture_file
    return render_template("home.html", postsRead=posts, picturesRead=picturesRead)


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
    

@app.route("/admin_panel")
@login_required
def admin_panel():
    messages = Support.query.all()
    return render_template('admin_panel.html', messageRead=messages, title="Admin Panel")
    

# route to delete
@app.route("/user_profile")
@login_required
def user_profile():
    return render_template('user_profile.html', user=current_user)




@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_post = Post(
                title   = form.title.data,
                content = form.content.data,
                author  = current_user,
            )
            db.session.add(new_post)
            db.session.commit()
            flash('Your post has been created!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Some errors appeared, try again!', category='danger')
        
    return render_template('create_post.html',
                           title='New Post', 
                           form=form,
                           legend='New Post')


@app.route("/post/<int:post_id>") # id конкретного поста
def post(post_id): # id конкретного поста
    post = Post.query.get_or_404(post_id) # формує дані конкретного поста по його id і передає в темплейт post.html
                                          # Якщо пост по id не буде знайдено виведе помилку 404
    return render_template('post.html', title=post.title, post=post)



@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id): 
    post = Post.query.get_or_404(post_id)# Шукає пост за id або викидає 404 
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() # just updating existing data, so no db.add here 
        flash('Your post has been updated', 'success')
        return redirect(url_for('post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',
                           title='Update Post', 
                           form=form,
                           legend='Update Post')
    
    
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id): 
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
    
    

@app.route("/user/<string:username>") 
def user(username):
    page = request.args.get('page', 1, type=int)
    
    user = User.query.filter_by(username=username).first_or_404()
    
    posts = Post.query.filter_by(user_id=user.id).\
        order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=2)
    
    return render_template("user.html", user=user, posts=posts)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request(): # here user will enter email to send email for passw reset
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info') # blue
        return redirect(url_for('login'))
    return render_template("reset_request.html", title="Reset Password", form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):  # here user will actually reset it's passw 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is invalid or expired token', 'warning') # yellow
        return render_template("reset_request.html")
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! Now you are able to login.', 'success')
        return redirect(url_for('login'))
    return render_template("reset_token.html", title="Reset Password", form=form)


