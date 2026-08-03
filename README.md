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

## Quick start (local)

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy config.example.py config.py
flask --app run:app db upgrade
python run.py
```

Open http://127.0.0.1:5000

## Deploy to Render + Neon (free portfolio hosting)

### 1. Neon (database)

1. Create a project at [neon.tech](https://neon.tech)
2. Copy the **connection string** (PostgreSQL)
3. If it starts with `postgres://`, the app fixes it automatically

### 2. Render (web app)

1. Push this repo to GitHub
2. On [render.com](https://render.com): **New → Blueprint** (uses `render.yaml`)  
   Or **New → Web Service** and connect the repo manually:
   - **Build command:** `pip install -r requirements.txt && flask --app run:app db upgrade`
   - **Start command:** `gunicorn run:app`
3. Set environment variables in Render:

| Variable | Value |
|---|---|
| `DATABASE_URL` | Neon connection string |
| `SECRET_KEY` | long random string (Render can auto-generate) |
| `PROFILE_UPLOADS_ENABLED` | `false` |
| `EMAIL_USER` / `EMAIL_PASS` | optional, for password reset |

4. After first deploy, seed categories and promote admin (Render shell or one-off):

```python
from flaskstart import app
from flaskstart.utils.db_seed import seed_categories, promote_admin_accounts
with app.app_context():
    seed_categories()
    promote_admin_accounts()
```

**Note:** Free Render apps sleep after ~15 min idle (30–60s cold start). Profile picture uploads are disabled in production (`PROFILE_UPLOADS_ENABLED=false`).

## Database migrations

```powershell
flask --app run:app db migrate -m "message"
flask --app run:app db upgrade
```

## Admin access

Users with `role = admin` can access `/admin_panel`.

## Tests

```powershell
pytest
```

## Tech stack

Flask, SQLAlchemy, PostgreSQL, Flask-Login, Flask-Migrate, Gunicorn, Bootstrap 5, pytest
