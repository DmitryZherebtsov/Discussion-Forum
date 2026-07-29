def parse_tags(tag_string):
    if not tag_string:
        return []
    return [tag.strip().lower() for tag in tag_string.split(',') if tag.strip()]


def assign_tags(post, tag_string):
    from flaskstart import db
    from flaskstart.models import Tag

    names = parse_tags(tag_string)
    tags = []
    for name in names:
        tag = Tag.query.filter_by(name=name).first()
        if not tag:
            tag = Tag(name=name)
            db.session.add(tag)
        tags.append(tag)
    post.tags = tags
