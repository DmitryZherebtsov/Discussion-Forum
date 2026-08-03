"""Seed the database with demo users, posts, comments, likes, and support messages."""

import sys

from flaskstart import app
from flaskstart.models import User
from flaskstart.utils.db_seed import seed_demo_data

if __name__ == '__main__':
    with app.app_context():
        force = '--force' in sys.argv
        if User.query.count() > 0 and not force:
            print('Database already has users. Run: python seed_db.py --force')
        else:
            seed_demo_data(force=True)
