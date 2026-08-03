import pytest

from flaskstart import app, db
from flaskstart.models import Category, Comment, Like, Post, User
from flaskstart.utils.db_seed import promote_admin_accounts, seed_categories


@pytest.fixture
def client():
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
        'ADMIN_EMAIL': 'admin@test.com',
        'SEED_DEMO_DATA': False,
    })

    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_categories()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def create_user(username, email, password='password123', role='user', can_post=False):
    from flaskstart import bcrypt

    if role == 'admin':
        can_post = True
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(
        username=username,
        email=email,
        password=hashed,
        role=role,
        can_post=can_post,
    )
    db.session.add(user)
    db.session.commit()
    return user


def login(client, email, password='password123'):
    return client.post('/login', data={'email': email, 'password': password}, follow_redirects=True)


@pytest.fixture
def admin_user(client):
    with app.app_context():
        return create_user('adminuser', 'admin@test.com', role='admin')


@pytest.fixture
def regular_user(client):
    with app.app_context():
        return create_user('regularuser', 'user@test.com', can_post=True)


@pytest.fixture
def pending_user(client):
    with app.app_context():
        return create_user('pendinguser', 'pending@test.com', can_post=False)


def test_register_and_login(client):
    response = client.post('/register', data={
        'username': 'newbie',
        'email': 'newbie@test.com',
        'password': 'password123',
        'confirm_password': 'password123',
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.post('/login', data={
        'email': 'newbie@test.com',
        'password': 'password123',
    }, follow_redirects=True)
    assert b'Log out' in response.data


def test_owner_registration_becomes_admin(client):
    response = client.post('/register', data={
        'username': 'owner',
        'email': 'admin@test.com',
        'password': 'password123',
        'confirm_password': 'password123',
    }, follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(email='admin@test.com').first()
        assert user.role == 'admin'
        assert user.can_post is True


def test_create_post_requires_login(client):
    response = client.get('/post/new', follow_redirects=True)
    assert b'Login' in response.data


def test_create_post_requires_approval(client, pending_user):
    login(client, 'pending@test.com')
    response = client.get('/post/new', follow_redirects=True)
    assert b'admin approval' in response.data


def test_create_post_with_tags_and_category(client, regular_user):
    with app.app_context():
        category = Category.query.filter_by(name='Technology').first()
        login(client, 'user@test.com')
        response = client.post('/post/new', data={
            'title': 'Test Post',
            'content': 'Post content here',
            'category': category.id,
            'tags': 'python, flask',
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Test Post' in response.data
        post = Post.query.filter_by(title='Test Post').first()
        assert post is not None
        assert len(post.tags) == 2


def test_admin_can_approve_posting(client, admin_user, pending_user):
    with app.app_context():
        login(client, 'admin@test.com')
        user = User.query.filter_by(email='pending@test.com').first()
        response = client.post(
            f'/admin_panel/user/{user.id}/approve_posting',
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert User.query.filter_by(email='pending@test.com').first().can_post is True


def test_search_posts(client, regular_user):
    with app.app_context():
        login(client, 'user@test.com')
        client.post('/post/new', data={
            'title': 'UniqueSearchTitle',
            'content': 'hello world',
            'category': 0,
            'tags': '',
        }, follow_redirects=True)
        response = client.get('/home?q=UniqueSearchTitle')
        assert b'UniqueSearchTitle' in response.data


def test_comment_and_like(client, regular_user):
    with app.app_context():
        login(client, 'user@test.com')
        client.post('/post/new', data={
            'title': 'Interactive Post',
            'content': 'content',
            'category': 0,
            'tags': '',
        }, follow_redirects=True)
        post = Post.query.filter_by(title='Interactive Post').first()

        response = client.post(f'/post/{post.id}/comment', data={'content': 'Nice post!'}, follow_redirects=True)
        assert b'Nice post!' in response.data
        assert Comment.query.count() == 1

        client.post(f'/post/{post.id}/like', follow_redirects=True)
        assert Like.query.count() == 1


def test_admin_panel_forbidden_for_regular_user(client, regular_user):
    with app.app_context():
        login(client, 'user@test.com')
        response = client.get('/admin_panel')
        assert response.status_code == 403


def test_admin_panel_accessible_for_admin(client, admin_user):
    with app.app_context():
        login(client, 'admin@test.com')
        response = client.get('/admin_panel')
        assert response.status_code == 200
        assert b'Admin Panel' in response.data


def test_promote_admin_accounts(client):
    with app.app_context():
        app.config['ADMIN_EMAIL'] = 'admin@gmail.com'
        user = create_user('Admin', 'admin@gmail.com')
        assert user.role == 'user'
        promote_admin_accounts()
        assert User.query.filter_by(username='Admin').first().role == 'admin'
