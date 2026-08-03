# DiscussionForum

Flask discussion forum — portfolio project with auth, posts, comments, likes, tags, categories, search, and admin moderation.

Live - https://discussion-forum-mmq1.onrender.com/home

## Features

- User registration, login, profile pictures, password reset
- Posts with categories and tags
- Comments and likes
- Search and filter by tag/category
- Role-based admin panel
- Flask-Migrate database migrations
- Light/dark theme
- pytest test suite

  <img width="1597" height="731" alt="image" src="https://github.com/user-attachments/assets/02e40c84-0e0e-4143-b989-e56f470ee07d" />
  <img width="883" height="693" alt="image" src="https://github.com/user-attachments/assets/82b99a2f-dd6c-407e-8948-7af81935ae87" />
  <img width="1353" height="736" alt="image" src="https://github.com/user-attachments/assets/3a7d6fd1-234a-41e8-87c8-cc5f5b22bac5" />


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

Optional demo data (7 users, 25 posts, comments, likes):

```powershell
python seed_db.py
```

Demo admin: `admin@gmail.com` / `123`

## Deploy to Render + Neon (free portfolio hosting)

**Deploy from the `master` branch.** It has the current app (migrations, admin panel, comments, likes, tags, Render config). The `dev` branch is outdated and should not be used for production.

### 1. Neon (database)

1. Create a project at [neon.tech](https://neon.tech)
2. Copy the **connection string** (PostgreSQL)
3. If it starts with `postgres://`, the app fixes it automatically

### 2. Render (web app)

1. Push this repo to GitHub (make sure `master` is up to date)
2. On [render.com](https://render.com): **New → Blueprint** (uses `render.yaml`, branch `master`)  
   Or **New → Web Service**, connect the repo, and set **Branch** to `master`:
   - **Build command:** `cp config.example.py config.py && pip install -r requirements.txt && flask --app run:app db upgrade`
   - **Start command:** `gunicorn run:app`
3. Set environment variables in Render:

| Variable | Value |
|---|---|
| `DATABASE_URL` | Neon connection string |
| `SECRET_KEY` | long random string (Render can auto-generate) |
| `PROFILE_UPLOADS_ENABLED` | `false` |
| `EMAIL_USER` / `EMAIL_PASS` | optional, for password reset emails |

Migrations run automatically during the build — you do not need to run them manually on Render.

**Demo data loads automatically** on first startup when the database has no users (7 users, 25 posts, comments, likes, support messages). To re-seed manually in Render Shell: `python seed_db.py --force`

### 3. After first deploy

If auto-seed ran, log in with demo accounts (password for all: `123`):

| Account | Email |
|---|---|
| Admin | `admin@gmail.com` |
| NoraTravel | `nora.travel@example.com` |
| KaiRunner | `kai.runner@example.com` |
| … | (see `db_seed.py` for full list) |

**Option A — use your own account instead**

1. Register on the live site
2. In Render **Shell**, promote yourself to admin (replace the email):

```python
from flaskstart import app, db
from flaskstart.models import User
from flaskstart.utils.db_seed import seed_categories
with app.app_context():
    seed_categories()
    user = User.query.filter_by(email="your@email.com").one()
    user.role = "admin"
    db.session.commit()
```

**Option B — reload demo content manually**

In Render **Shell**:

```bash
python seed_db.py --force
```

This replaces all users/posts with the portfolio demo dataset. Admin login: `admin@gmail.com` / `123`.

**Notes**

- Free Render apps sleep after ~15 min idle (~30–60s cold start).
- Profile picture uploads are disabled in production (`PROFILE_UPLOADS_ENABLED=false`); avatars use bundled defaults.
- Password reset requires `EMAIL_USER` and `EMAIL_PASS` (Gmail SMTP).

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
