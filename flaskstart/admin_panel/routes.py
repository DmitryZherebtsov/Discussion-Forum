from flask import Blueprint, render_template
from flask_login import login_required

from flaskstart.models import Support

adminpanel = Blueprint('adminpanel', __name__) # instance of Blueprint

@adminpanel.route("/admin_panel")
@login_required
def admin_panel():
    messages = Support.query.all()
    return render_template('admin_panel.html', messageRead=messages, title="Admin Panel")
