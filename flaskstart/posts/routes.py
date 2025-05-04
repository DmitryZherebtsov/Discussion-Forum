from flask import (render_template, request,
                   url_for, flash, redirect, abort, Blueprint)
from flaskstart import db
from flask_login import current_user, login_required
from flaskstart.models import Post
from flaskstart.posts.forms import PostForm

posts = Blueprint('posts', __name__) # instance of Blueprint


@posts.route("/post/new", methods=['GET', 'POST'])
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
            return redirect(url_for('main.home'))
        else:
            flash('Some errors appeared, try again!', category='danger')
        
    return render_template('create_post.html',
                           title='New Post', 
                           form=form,
                           legend='New Post')


@posts.route("/post/<int:post_id>") # id конкретного поста
def post(post_id): # id конкретного поста
    post = Post.query.get_or_404(post_id) # формує дані конкретного поста по його id і передає в темплейт post.html
                                          # Якщо пост по id не буде знайдено виведе помилку 404
    return render_template('post.html', title=post.title, post=post)



@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',
                           title='Update Post', 
                           form=form,
                           legend='Update Post')
    
    
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id): 
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
    


