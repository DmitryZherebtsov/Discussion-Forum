# DiscussionForum

Flask discussion forum — portfolio project with auth, posts, comments, likes, tags, categories, search, and admin moderation.

## Features

- User registration, login, profile pictures, password reset
- Posts with categories and tags
- Comments and likes
- Search and filter by tag/category
- Role-based admin panel
- Flask-Migrate database migrations
- pytest test suite

## Quick start

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy config.example.py config.py
flask --app run:app db upgrade
python run.py
```

Open http://127.0.0.1:5000

## Database migrations

```powershell
flask --app run:app db init          # first time only
flask --app run:app db migrate -m "message"
flask --app run:app db upgrade
```

After upgrading an existing database, promote legacy admin accounts once from the admin panel or run:

```python
from flaskstart.utils.db_seed import seed_categories, promote_admin_accounts
seed_categories()
promote_admin_accounts()
```

## Admin access

Users with `role = admin` can access `/admin_panel`. The legacy `Admin` user or `admin@gmail.com` account can be promoted via the seed helper above.

## Tests

```powershell
pytest
```

## Tech stack

Flask, SQLAlchemy, Flask-Login, Flask-Migrate, WTForms, Bootstrap 5, pytest
