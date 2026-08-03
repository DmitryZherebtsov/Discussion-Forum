# DiscussionForum

Flask discussion forum — portfolio project with auth, posts, comments, likes, tags, categories, search, and admin moderation.

## Features

- User registration, login, profile pictures, password reset
- Posts with categories and tags
- Comments and likes
- Search and filter by tag/category
- Role-based admin panel
- **Posting approval** — new users must be approved before they can create posts
- **Owner-only admin** — only `ADMIN_EMAIL` can be site admin
- Flask-Migrate database migrations
- Light/dark theme
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
| `ADMIN_EMAIL` | **your email** — only this account becomes admin |
| `SEED_DEMO_DATA` | `false` for production (no public demo accounts) |
| `EMAIL_USER` / `EMAIL_PASS` | optional, for password reset emails |

Migrations run automatically during the build.

### 3. After first deploy

1. Set `ADMIN_EMAIL` to the email you will register with
2. Register on the live site with that exact email → you become **admin** automatically
3. Other users can register but **cannot post** until you click **Allow posting** in Admin Panel

Optional demo data for local/testing only — set `SEED_DEMO_DATA=true` and run `python seed_db.py --force`

**Do not** use demo admin `admin@gmail.com` / `123` on a public site.

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

Only the user whose email matches `ADMIN_EMAIL` is admin. Approve posting for other users in `/admin_panel`.

## Tests

```powershell
pytest
```

## Tech stack

Flask, SQLAlchemy, PostgreSQL, Flask-Login, Flask-Migrate, Gunicorn, Bootstrap 5, pytest
