import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _normalize_database_url(url):
    if url and url.startswith('postgres://'):
        return url.replace('postgres://', 'postgresql://', 1)
    return url


def _default_sqlite_uri():
    db_path = os.path.join(BASE_DIR, 'site.db').replace('\\', '/')
    return f'sqlite:///{db_path}'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-me-to-a-random-secret-key'

    SQLALCHEMY_DATABASE_URI = _normalize_database_url(
        os.environ.get('DATABASE_URL')
    ) or _default_sqlite_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Profile uploads use local disk — disable on Render (ephemeral filesystem)
    PROFILE_UPLOADS_ENABLED = os.environ.get('PROFILE_UPLOADS_ENABLED', 'true').lower() == 'true'

    # Gmail SMTP settings for password reset emails
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    # Only this email can be site admin (set on Render to your email)
    ADMIN_EMAIL = (os.environ.get('ADMIN_EMAIL') or '').strip().lower()

    # Demo seed: on by default for local SQLite, off when DATABASE_URL is set (Render/Neon)
    _seed_default = 'false' if os.environ.get('DATABASE_URL') else 'true'
    SEED_DEMO_DATA = os.environ.get('SEED_DEMO_DATA', _seed_default).lower() == 'true'
