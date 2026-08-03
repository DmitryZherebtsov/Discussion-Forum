import os

from sqlalchemy import inspect, text


def _seed_if_empty(app, db):
    from flaskstart.utils.admin_access import sync_owner_admin
    from flaskstart.utils.db_seed import seed_categories, seed_demo_data

    seed_categories()

    inspector = inspect(db.engine)
    if not inspector.has_table('user'):
        return

    user_count = db.session.execute(text('SELECT COUNT(*) FROM "user"')).scalar()
    if user_count == 0 and app.config.get('SEED_DEMO_DATA'):
        seed_demo_data(force=True)

    sync_owner_admin(app, db)


def ensure_database(app, db):
    """Create missing tables and optionally seed demo data on an empty database."""
    if app.config.get('TESTING'):
        return

    with app.app_context():
        uri = app.config['SQLALCHEMY_DATABASE_URI']
        if uri.startswith('sqlite:///'):
            db_path = uri.replace('sqlite:///', '')
            if os.path.exists(db_path) and os.path.getsize(db_path) == 0:
                os.remove(db_path)

        inspector = inspect(db.engine)
        if inspector.has_table('post'):
            _seed_if_empty(app, db)
            return

        if inspector.has_table('alembic_version'):
            db.session.execute(text('DELETE FROM alembic_version'))
            db.session.commit()

        from flask_migrate import upgrade
        upgrade()

        inspector = inspect(db.engine)
        if not inspector.has_table('post'):
            db.create_all()

        _seed_if_empty(app, db)
