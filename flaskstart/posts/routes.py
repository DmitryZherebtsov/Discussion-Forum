from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from flaskstart import db
from flaskstart.models import Comment, Like, Post
from flaskstart.posts.forms import CommentForm, PostForm
from flaskstart.posts.utils import assign_tags
from flaskstart.utils.permissions import can_manage_comment, can_manage_post, posting_required

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
@posting_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user,
            category_id=None if form.category.data == 0 else form.category.data,
        )
        db.session.add(post)
        db.session.flush()
        assign_tags(post, form.tags.data)
        db.session.commit()
        flash('Your post has been created!', category='success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comment_form = CommentForm()
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_posted.asc()).all()
    return render_template(
        'post.html',
        title=post.title,
        post=post,
        comments=comments,
        comment_form=comment_form,
    )


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
@posting_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if not can_manage_post(post):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category_id = None if form.category.data == 0 else form.category.data
        assign_tags(post, form.tags.data)
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category_id or 0
        form.tags.data = ', '.join(tag.name for tag in post.tags)
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if not can_manage_post(post):
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted!', 'danger')
    return redirect(url_for('main.home'))


@posts.route("/post/<int:post_id>/comment", methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added.', 'success')
    else:
        flash('Could not add comment.', 'danger')
    return redirect(url_for('posts.post', post_id=post_id))


@posts.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not can_manage_comment(comment):
        abort(403)
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'info')
    return redirect(url_for('posts.post', post_id=post_id))


@posts.route("/post/<int:post_id>/like", methods=['POST'])
@login_required
def toggle_like(post_id):
    post = Post.query.get_or_404(post_id)
    existing = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if existing:
        db.session.delete(existing)
        flash('Like removed.', 'info')
    else:
        db.session.add(Like(user_id=current_user.id, post_id=post.id))
        flash('Post liked!', 'success')
    db.session.commit()
    return redirect(request.referrer or url_for('posts.post', post_id=post_id))
