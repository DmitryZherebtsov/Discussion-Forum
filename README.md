# DiscussionForum

Flask-based discussion forum with user accounts, posts, support messages, and an admin panel.

## Features

- User registration, login, and profile pictures
- Create, read, update, and delete posts
- Password reset via email
- Support messages to admin
- Admin panel (`admin@gmail.com` only)

## Setup

### 1. Clone the repository

Use `git clone` instead of downloading a ZIP so you keep Git history:

```powershell
git clone https://github.com/YOUR_USERNAME/DiscussionForum.git
cd DiscussionForum
```

If you already have the files locally without Git:

```powershell
git init
git remote add origin https://github.com/YOUR_USERNAME/DiscussionForum.git
git fetch origin
git checkout -b main origin/main
```

### 2. Create a virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure secrets

Copy the example config and edit it with your values:

```powershell
copy config.example.py config.py
```

Edit `config.py`:

- Set a strong `SECRET_KEY` (random string)
- For password reset emails, set `MAIL_USERNAME` and `MAIL_PASSWORD`, or use environment variables:

```powershell
$env:EMAIL_USER = "your@gmail.com"
$env:EMAIL_PASS = "your-app-password"
```

`config.py` is gitignored and should never be committed.

### 4. Add static assets (if missing)

Place these files in `flaskstart/static/`:

- `profile_pics/default.jpg` — default avatar for new users
- `cat_error.png` — used on error pages (403, 404, 500)

### 5. Run the app

```powershell
python run.py
```

Open http://127.0.0.1:5000 in your browser.

The SQLite database (`site.db`) is created automatically on first run.

## Admin access

Register a user with email `admin@gmail.com` to access the admin panel at `/admin_panel`.

## Project structure

```
DiscussionForum/
├── config.example.py      # Config template (committed)
├── config.py              # Your secrets (gitignored)
├── run.py                 # Entry point
├── requirements.txt
└── flaskstart/
    ├── __init__.py        # App setup and blueprint registration
    ├── models.py          # User, Post, Support models
    ├── main/              # Home page
    ├── users/             # Auth and account
    ├── posts/             # Post CRUD
    ├── support/           # Support messages
    ├── admin_panel/       # Admin view
    ├── errors/            # Error handlers
    ├── static/            # CSS and uploads
    └── templates/         # HTML templates
```

## Git workflow

- **`main`** — stable working code
- **Feature branches** — `feature/my-change` for new work
- **Never commit** — `config.py`, `.env`, `*.db`, uploaded profile pictures

## Tech stack

- Flask 3, SQLAlchemy, Flask-Login, Flask-Bcrypt, Flask-Mail
- WTForms, Pillow
- Bootstrap 5
