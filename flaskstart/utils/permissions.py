from functools import wraps

from flask import abort, flash, redirect, url_for
from flask_login import current_user


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)

    return wrapped


def user_can_post(user=None):
    user = user or current_user
    if not user or not user.is_authenticated:
        return False
    return user.can_create_posts


def posting_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)
        if not user_can_post():
            flash('You need admin approval before you can create or edit posts.', 'warning')
            return redirect(url_for('main.home'))
        return view(*args, **kwargs)

    return wrapped


def can_manage_post(post):
    if not current_user.is_authenticated:
        return False
    if current_user.is_admin:
        return True
    return post.author == current_user and user_can_post()


def can_manage_comment(comment):
    return current_user.is_authenticated and (
        comment.author == current_user or current_user.is_admin
    )
