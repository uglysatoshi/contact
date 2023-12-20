from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SellingForm(FlaskForm):
    item = StringField(validators=[DataRequired()])
    status = StringField(validators=[DataRequired()])
    submit = SubmitField("Add new selling")
