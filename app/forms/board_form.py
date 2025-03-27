from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class BoardForm(FlaskForm):

    # Name
    name = StringField(
        "name",
        validators=[
            DataRequired(message="Name is required"),
            Length(max=50, message="Name should be within 50 characters"),
        ],
    )
