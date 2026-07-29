from flask import render_template, request, Blueprint
from sqlalchemy import or_

from flaskstart.models import Category, Post, Tag

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '', type=str).strip()
    tag_name = request.args.get('tag', '', type=str).strip().lower()
    category_id = request.args.get('category', 0, type=int)

    query = Post.query

    if search:
        query = query.filter(
            or_(Post.title.ilike(f'%{search}%'), Post.content.ilike(f'%{search}%'))
        )

    if tag_name:
        query = query.join(Post.tags).filter(Tag.name == tag_name)

    if category_id:
        query = query.filter(Post.category_id == category_id)

    posts = query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    tags = Tag.query.order_by(Tag.name).all()
    categories = Category.query.order_by(Category.name).all()

    return render_template(
        'home.html',
        postsRead=posts,
        tags=tags,
        categories=categories,
        search=search,
        active_tag=tag_name,
        active_category=category_id,
    )


@main.route("/about")
def about():
    return render_template("about.html", title="About")
