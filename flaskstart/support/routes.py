
from flask import flash, render_template, request, redirect, url_for, Blueprint
from flaskstart import db
from flaskstart.support.forms import SupportFrom
from flaskstart.models import Support
from flask_login import current_user, login_required

support_page = Blueprint('support_page', __name__) # instance of Blueprint

@support_page.route("/support", methods=['GET', 'POST'])
@login_required
def support():
    form = SupportFrom()
    if request.method == 'POST':
        if form.validate_on_submit():
            message = Support(title=form.title.data,
                              message=form.message.data,
                              user_id = current_user.id )
            db.session.add(message)
            db.session.commit()
            flash(f'Your message has been successfully sent to the administrator!', 'success')
            return redirect(url_for('main.home'))
        else:
            print("*********** \n Form errors:", form.errors, "\n **********")
            flash(f'Fail to send your message! *_* ', 'danger')

    return render_template('support.html', title='Support', form=form)
    