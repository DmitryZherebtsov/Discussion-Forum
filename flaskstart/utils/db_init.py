import os

from sqlalchemy import inspect, text


def ensure_database(app, db):
    """Create missing tables. Repairs broken DBs where alembic_version exists but tables don't."""
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
            return

        if inspector.has_table('alembic_version'):
            db.session.execute(text('DELETE FROM alembic_version'))
            db.session.commit()

        from flask_migrate import upgrade
        upgrade()

        inspector = inspect(db.engine)
        if not inspector.has_table('post'):
            db.create_all()

        from flaskstart.utils.db_seed import seed_categories
        seed_categories()

        if db.session.execute(text('SELECT COUNT(*) FROM "user"')).scalar() == 0:
            from flaskstart.utils.db_seed import seed_demo_data
            seed_demo_data(force=True)
