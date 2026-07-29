from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from flaskstart.models import Category


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[Optional()])
    tags = StringField('Tags (comma separated)', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Publish')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [(0, 'None')] + [
            (category.id, category.name)
            for category in Category.query.order_by(Category.name).all()
        ]


class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Post Comment')
