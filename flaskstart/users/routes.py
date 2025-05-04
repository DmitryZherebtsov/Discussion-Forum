from flask import (render_template, request,
                   url_for, flash, redirect, Blueprint)
from flaskstart import db, bcrypt
from flask_login import current_user, login_required, login_user, logout_user
from flaskstart.users.forms import (RegitrationForm, LoginForm, UpdateAccountForm,
                                    RequestResetForm, ResetPasswordForm)
from flaskstart.models import User, Post
from flaskstart.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__) # instance of Blueprint


@users.route("/register", methods=['GET', 'POST']) # REGISTER ##########
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegitrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You can login now by the name: {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST']) # LOGIN ##########
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # беру першого юзера по мейлу який він ввів
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
                                    #  if next_page not none
        else:
            flash('Login Failed, check your email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users.route("/account", methods=['GET', 'POST']) # UPDATE USER INFO ##########
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET': # заповнити поля поточними даними
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', 
                           title='Account', 
                           image_file=image_file, 
                           form=form )

     
     

@users.route("/user/<string:username>") 
def user(username):
    page = request.args.get('page', 1, type=int)
    
    user = User.query.filter_by(username=username).first_or_404()
    
    posts = Post.query.filter_by(user_id=user.id).\
        order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=2)
    
    return render_template("user.html", user=user, posts=posts)
     
     
     
     

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request(): # here user will enter email to send email for passw reset
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info') # blue
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):  # here user will actually reset it's passw 
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
        return redirect(url_for('users.login'))
    return render_template("reset_token.html", title="Reset Password", form=form)
