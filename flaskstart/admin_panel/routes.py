from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from flaskstart import db
from flaskstart.models import Comment, Post, Support, User
from flaskstart.utils.db_seed import promote_admin_accounts
from flaskstart.utils.permissions import admin_required

adminpanel = Blueprint('adminpanel', __name__)


@adminpanel.route("/admin_panel")
@login_required
@admin_required
def admin_panel():
    stats = {
        'users': User.query.count(),
        'posts': Post.query.count(),
        'comments': Comment.query.count(),
        'support_messages': Support.query.count(),
    }
    users = User.query.order_by(User.username).all()
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    comments = Comment.query.order_by(Comment.date_posted.desc()).all()
    messages = Support.query.order_by(Support.date_posted.desc()).all()
    return render_template(
        'admin_panel.html',
        title="Admin Panel",
        stats=stats,
        users=users,
        posts=posts,
        comments=comments,
        messageRead=messages,
    )


@adminpanel.route("/admin_panel/user/<int:user_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'warning')
        return redirect(url_for('adminpanel.admin_panel'))
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} deleted.', 'success')
    return redirect(url_for('adminpanel.admin_panel'))


@adminpanel.route("/admin_panel/user/<int:user_id>/toggle_admin", methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot change your own role.', 'warning')
        return redirect(url_for('adminpanel.admin_panel'))
    user.role = 'user' if user.is_admin else 'admin'
    db.session.commit()
    flash(f'{user.username} is now {"an admin" if user.is_admin else "a regular user"}.', 'info')
    return redirect(url_for('adminpanel.admin_panel'))


@adminpanel.route("/admin_panel/post/<int:post_id>/delete", methods=['POST'])
@login_required
@admin_required
def admin_delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted by admin.', 'success')
    return redirect(url_for('adminpanel.admin_panel'))


@adminpanel.route("/admin_panel/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
@admin_required
def admin_delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted by admin.', 'success')
    return redirect(url_for('adminpanel.admin_panel'))


@adminpanel.route("/admin_panel/support/<int:message_id>/delete", methods=['POST'])
@login_required
@admin_required
def admin_delete_support(message_id):
    message = Support.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('Support message deleted.', 'success')
    return redirect(url_for('adminpanel.admin_panel'))


@adminpanel.route("/admin_panel/promote_legacy_admins", methods=['POST'])
@login_required
@admin_required
def promote_legacy_admins():
    promote_admin_accounts()
    flash('Legacy admin accounts updated.', 'info')
    return redirect(url_for('adminpanel.admin_panel'))
