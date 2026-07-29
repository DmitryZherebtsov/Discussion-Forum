from functools import wraps

from flask import abort
from flask_login import current_user


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)

    return wrapped


def can_manage_post(post):
    return current_user.is_authenticated and (
        post.author == current_user or current_user.is_admin
    )


def can_manage_comment(comment):
    return current_user.is_authenticated and (
        comment.author == current_user or current_user.is_admin
    )
