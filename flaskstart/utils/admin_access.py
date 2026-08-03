from flaskstart.models import User


def get_admin_email(app):
    return (app.config.get('ADMIN_EMAIL') or '').strip().lower()


def apply_owner_privileges(user, app):
    """Grant admin + posting rights only to the configured owner email."""
    admin_email = get_admin_email(app)
    if admin_email and user.email.lower() == admin_email:
        user.role = 'admin'
        user.can_post = True
        return True
    return user.is_admin


def sync_owner_admin(app, db):
    """Ensure only ADMIN_EMAIL can be admin. Owner always can post."""
    admin_email = get_admin_email(app)
    if not admin_email:
        return

    for user in User.query.filter_by(role='admin').all():
        if user.email.lower() != admin_email:
            user.role = 'user'

    owner = User.query.filter(db.func.lower(User.email) == admin_email).first()
    if owner:
        owner.role = 'admin'
        owner.can_post = True

    db.session.commit()
