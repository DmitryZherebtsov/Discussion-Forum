"""Seed the database with demo users, posts, comments, likes, and support messages."""

from flaskstart import app
from flaskstart.utils.db_seed import seed_demo_data

if __name__ == '__main__':
    with app.app_context():
        seed_demo_data(force=True)
