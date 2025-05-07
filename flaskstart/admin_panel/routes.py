from flask import Blueprint, abort, redirect, render_template, url_for
from flask_login import current_user, login_required

from flaskstart.models import Support

adminpanel = Blueprint('adminpanel', __name__) # instance of Blueprint

@adminpanel.route("/admin_panel")
@login_required
def admin_panel():
    messages = Support.query.all()
    if current_user.email != "admin@gmail.com":
        abort(403)
    return render_template('admin_panel.html', messageRead=messages, title="Admin Panel")
