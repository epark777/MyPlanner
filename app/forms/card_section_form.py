from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CardSectionForm(FlaskForm):
    """Form for creating and updating card sections"""
    
    title = StringField(
        "title",
        validators=[
            DataRequired(message="Title is required"),
            Length(max=50, message="Title should be within 50 characters"),
        ],
    )