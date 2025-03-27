from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from datetime import datetime


class DateTimeValidator:

    def __init__(self, message=None):
        self.message = message or "Must be a valid ISO format date (YYYY-MM-DD)"

    def __call__(self, form, field):
        # Skip validation if field is empty
        if not field.data or field.data.strip() == "":
            return

        try:
            # Convert string to datetime object
            date_value = datetime.fromisoformat(field.data)

            # Update field data with parsed datetime object
            field.data = date_value

        except ValueError:
            # Log error for debugging
            print(f"Error parsing date: {field.data}")
            raise ValidationError(self.message)


class CardForm(FlaskForm):

    # Name
    name = StringField(
        label="Card Title",
        validators=[
            DataRequired(message="A title is required for this card"),
            Length(max=50, message="Title must be 50 characters or less"),
        ],
    )

    # Labels
    labels = StringField(
        label="Card Labels",
        validators=[
            Optional(),
            Length(max=50, message="Labels must be 50 characters or less"),
        ],
    )

    # Card Descriptions
    description = TextAreaField(
        label="Card Description",
        validators=[
            Optional(),
            Length(max=500, message="Description must be 500 characters or less"),
        ],
    )

    # Order
    order = IntegerField(label="Display Order", validators=[Optional()])

    # Date Date
    due_date = StringField(
        label="Due Date",
        validators=[
            Optional(),
            DateTimeValidator(message="Please use a valid date format (YYYY-MM-DD)"),
        ],
    )
