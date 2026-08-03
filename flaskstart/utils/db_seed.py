from datetime import datetime, timedelta

from flaskstart import bcrypt, db
from flaskstart.models import Category, Comment, Like, Post, Support, Tag, User
from flaskstart.posts.utils import assign_tags

DEFAULT_CATEGORIES = ['General', 'Technology', 'News', 'Help', 'Other']

DEMO_PASSWORD = '123'

PROFILE_PICS = [
    '481bcb822f1da8c0.jpg',
    '896afe327891d570.jpg',
    '953c10ccb35d2c8a.png',
    '1fb7d9635c67173d.jpg',
]


def seed_categories():
    for name in DEFAULT_CATEGORIES:
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
    db.session.commit()


def promote_admin_accounts():
    for user in User.query.filter(
        (User.username == 'Admin') | (User.email == 'admin@gmail.com')
    ).all():
        user.role = 'admin'
    db.session.commit()


def _password_hash():
    return bcrypt.generate_password_hash(DEMO_PASSWORD).decode('utf-8')


def _create_user(username, email, image_file, role='user'):
    user = User(
        username=username,
        email=email,
        password=_password_hash(),
        image_file=image_file,
        role=role,
    )
    db.session.add(user)
    db.session.flush()
    return user


def _get_category(name):
    return Category.query.filter_by(name=name).first()


def _create_post(author, title, content, category_name, tag_names, days_ago=0):
    post = Post(
        title=title,
        content=content,
        author=author,
        category=_get_category(category_name),
        date_posted=datetime.utcnow() - timedelta(days=days_ago, hours=days_ago * 2),
    )
    db.session.add(post)
    db.session.flush()
    assign_tags(post, ', '.join(tag_names))
    return post


def seed_demo_data(force=False):
    if User.query.count() > 0 and not force:
        print('Database already has users. Run with force=True to re-seed.')
        return

    if force:
        Like.query.delete()
        Comment.query.delete()
        Support.query.delete()
        Post.query.delete()
        User.query.delete()
        Tag.query.delete()
        db.session.commit()

    seed_categories()

    admin = _create_user('Admin', 'admin@gmail.com', PROFILE_PICS[0], role='admin')
    nora = _create_user('NoraTravel', 'nora.travel@example.com', PROFILE_PICS[1])
    kai = _create_user('KaiRunner', 'kai.runner@example.com', PROFILE_PICS[2])
    luna = _create_user('LunaChef', 'luna.chef@example.com', PROFILE_PICS[3])
    marco = _create_user('MarcoPhoto', 'marco.photo@example.com', PROFILE_PICS[0])
    zoe = _create_user('ZoeDesign', 'zoe.design@example.com', PROFILE_PICS[1])
    felix = _create_user('FelixMusic', 'felix.music@example.com', PROFILE_PICS[2])
    db.session.commit()

    posts_data = [
        (admin, 'Community Guidelines 2026', 'Keep discussions friendly and on-topic. Report spam, respect privacy, and give constructive feedback.', 'General', ['community', 'rules'], 28),
        (nora, 'Weekend Trip Ideas Near the City', 'Short train rides, lakeside walks, and small museums make perfect one-day escapes without big planning.', 'General', ['travel', 'weekend', 'lifestyle'], 24),
        (kai, 'Morning Routine That Actually Sticks', 'Ten minutes of stretching, water first, and no phone for the first hour changed my energy levels.', 'General', ['health', 'habits', 'fitness'], 20),
        (luna, 'Quick Pasta Recipes for Busy Evenings', 'Garlic-oil spaghetti, lemon-pepper salmon pasta, and creamy mushroom tagliatelle in under 25 minutes.', 'General', ['cooking', 'food', 'recipes'], 16),
        (zoe, 'Minimal Desk Setup for Focus', 'One monitor, warm lamp, cable tray, and a plant. Less clutter helped me study longer without burnout.', 'General', ['productivity', 'design', 'workspace'], 12),

        (felix, 'Best Free Tools for Learning Python', 'VS Code, official docs, Replit for quick tests, and small daily challenges beat marathon tutorials.', 'Technology', ['python', 'learning', 'tools'], 26),
        (marco, 'Phone Camera Tricks for Better Photos', 'Use grid lines, tap to expose faces, and shoot during golden hour. Editing lightly is enough.', 'Technology', ['photography', 'mobile', 'tips'], 22),
        (admin, 'Why We Moved to Database Migrations', 'Migrations make team changes safer and deployments repeatable. Never edit production schema manually.', 'Technology', ['flask', 'database', 'devops'], 18),
        (kai, 'Smartwatch vs Fitness App', 'I tested step accuracy and heart-rate tracking for a month. Both help, but consistency matters more.', 'Technology', ['fitness', 'gadgets', 'review'], 14),
        (nora, 'Useful Browser Extensions for Students', 'Grammar helpers, tab managers, and citation tools save hours during research-heavy weeks.', 'Technology', ['students', 'browser', 'productivity'], 8),

        (admin, 'Forum Update: Tags and Likes Live', 'You can now tag posts, like discussions, and filter by category. More moderation tools coming soon.', 'News', ['update', 'features', 'announcement'], 25),
        (luna, 'Local Food Festival This Saturday', 'Street food, live acoustic sets, and student discounts at the riverside market from 12:00 to 20:00.', 'News', ['event', 'food', 'local'], 19),
        (felix, 'New Album Releases Worth Hearing', 'Indie-electronic and modern jazz records dominated my playlist this month. Share your discoveries below.', 'News', ['music', 'albums', 'culture'], 15),
        (marco, 'City Marathon Registration Open', 'Early registration ends Friday. Volunteer spots are available if you prefer supporting runners.', 'News', ['sport', 'marathon', 'event'], 10),
        (zoe, 'Design Conference Highlights', 'Talks on accessible UI, color systems, and portfolio reviews were the most practical sessions.', 'News', ['design', 'conference', 'career'], 6),

        (kai, 'How to Track Running Progress?', 'Should I focus on pace, distance, or heart rate zones as a beginner with three runs per week?', 'Help', ['running', 'training', 'beginner'], 23),
        (nora, 'Best Travel Backpack Size?', 'I need a carry-on backpack for 4-day trips. What capacity works without overpacking?', 'Help', ['travel', 'gear', 'packing'], 17),
        (luna, 'Substitute for Heavy Cream?', 'Making soup tonight and forgot cream. What alternatives still give a rich texture?', 'Help', ['cooking', 'ingredients', 'tips'], 13),
        (felix, 'Learning Music Theory Online', 'Any structured courses or apps that helped you understand chords and composition?', 'Help', ['music', 'learning', 'theory'], 9),
        (marco, 'RAW or JPEG for Beginners?', 'My camera offers both formats. Is RAW worth the extra editing time when starting out?', 'Help', ['photography', 'camera', 'beginner'], 5),

        (zoe, 'Color Palettes That Work for Posters', 'Teal + coral, deep navy + sand, and monochrome with one accent color never fail me.', 'Other', ['design', 'colors', 'creativity'], 27),
        (felix, 'Songs for Late-Night Coding', 'Lo-fi, soft piano, and ambient soundtracks keep me focused without distracting lyrics.', 'Other', ['music', 'coding', 'playlist'], 21),
        (nora, 'Hidden Cafes Worth Visiting', 'Quiet corners, good espresso, and fast Wi-Fi. I mapped five favorites around campus.', 'Other', ['coffee', 'city', 'lifestyle'], 11),
        (luna, 'Comfort Food After Long Days', 'Tomato soup, grilled cheese, and simple rice bowls feel like a reset button in winter.', 'Other', ['food', 'comfort', 'winter'], 7),
        (kai, 'Trail Running in Autumn', 'Mud, colorful leaves, and cooler air. Safety tips: good shoes, tell someone your route, bring water.', 'Other', ['running', 'nature', 'season'], 3),
    ]

    created_posts = []
    for row in posts_data:
        created_posts.append(_create_post(*row))

    db.session.commit()

    comments_data = [
        (0, nora.id, 'Clear and helpful. Thanks for pinning this.'),
        (0, kai.id, 'Good reminder before posting heated replies.'),
        (1, luna.id, 'The lake route you mentioned is one of my favorites.'),
        (1, marco.id, 'I took photos there last weekend, stunning light.'),
        (5, admin.id, 'Start with small scripts and build one real mini-project.'),
        (5, zoe.id, 'Automate boring tasks first — that kept me motivated.'),
        (10, felix.id, 'Likes and tags make browsing much better now.'),
        (10, nora.id, 'Search by tag is super useful for travel posts.'),
        (15, kai.id, 'Distance first, pace later. Consistency beats speed early on.'),
        (15, admin.id, 'Try a simple log: date, distance, how you felt.'),
        (19, marco.id, 'Shoot JPEG while learning, switch to RAW when editing feels natural.'),
        (22, zoe.id, 'Your cafe map should become a pinned thread.'),
        (24, nora.id, 'Autumn trails are beautiful but slippery after rain — good tips.'),
    ]

    for post_index, user_id, content in comments_data:
        db.session.add(Comment(
            content=content,
            author=db.session.get(User, user_id),
            post=created_posts[post_index],
            date_posted=datetime.utcnow() - timedelta(hours=post_index + 6),
        ))

    likes_pairs = [
        (admin.id, 0), (nora.id, 0), (kai.id, 0), (luna.id, 0), (zoe.id, 0),
        (nora.id, 1), (marco.id, 1), (luna.id, 1),
        (kai.id, 2), (felix.id, 2), (admin.id, 2),
        (luna.id, 3), (nora.id, 3), (zoe.id, 3),
        (felix.id, 5), (admin.id, 5), (zoe.id, 5), (kai.id, 5),
        (marco.id, 6), (nora.id, 6),
        (admin.id, 10), (felix.id, 10), (nora.id, 10), (kai.id, 10), (luna.id, 10),
        (kai.id, 15), (admin.id, 15), (felix.id, 15),
        (zoe.id, 20), (marco.id, 20), (luna.id, 20),
        (nora.id, 22), (felix.id, 22), (kai.id, 22),
        (kai.id, 24), (nora.id, 24), (marco.id, 24), (luna.id, 24),
    ]

    seen = set()
    for user_id, post_index in likes_pairs:
        key = (user_id, created_posts[post_index].id)
        if key in seen:
            continue
        seen.add(key)
        db.session.add(Like(user_id=user_id, post_id=created_posts[post_index].id))

    support_data = [
        (nora.id, 'Feature idea: saved posts', 'Would love a bookmark button for travel threads I want to revisit later.'),
        (kai.id, 'Broken image on mobile', 'One profile avatar looked stretched on my phone during night mode.'),
        (felix.id, 'Thanks for the platform', 'The music and tech categories feel active. Great community vibe overall.'),
        (marco.id, 'Moderation question', 'Should photography self-promo links go in General or Other?'),
    ]

    for user_id, title, message in support_data:
        db.session.add(Support(
            title=title,
            message=message,
            user=db.session.get(User, user_id),
            date_posted=datetime.utcnow() - timedelta(days=1, hours=user_id),
        ))

    db.session.commit()
    promote_admin_accounts()

    print('Demo data seeded successfully.')
    print(f'Users: {User.query.count()}, Posts: {Post.query.count()}, '
          f'Comments: {Comment.query.count()}, Likes: {Like.query.count()}')
    print(f'All demo accounts use password: {DEMO_PASSWORD}')
    print('Admin login: admin@gmail.com')
