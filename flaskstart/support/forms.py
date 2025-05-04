from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import DataRequired, Length

class SupportFrom(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=5, max=100)
    ])
    message = TextAreaField('Message', validators=[
        DataRequired()
    ])
    submit = SubmitField('Send')
    
