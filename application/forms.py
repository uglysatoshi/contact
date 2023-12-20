from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired


class SellingForm(FlaskForm):
    item = StringField(validators=[DataRequired()])
    status = SelectField("Статус", choices=[("Открыт", "Открыт"), ("Закрыт", "Закрыт"), ("Выполняется", "Выполняется")], validators=[DataRequired()])
    submit = SubmitField("Добавить продажу")
