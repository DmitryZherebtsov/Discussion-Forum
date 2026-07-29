DEFAULT_CATEGORIES = ['General', 'Technology', 'News', 'Help', 'Other']


def seed_categories():
    from flaskstart import db
    from flaskstart.models import Category

    for name in DEFAULT_CATEGORIES:
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
    db.session.commit()


def promote_admin_accounts():
    from flaskstart import db
    from flaskstart.models import User

    for user in User.query.filter(
        (User.username == 'Admin') | (User.email == 'admin@gmail.com')
    ).all():
        user.role = 'admin'
    db.session.commit()
