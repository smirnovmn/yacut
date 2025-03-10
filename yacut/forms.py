from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields import StringField
from wtforms.validators import Length, Optional


class UrlMapForm(FlaskForm):
    original_link = StringField(
        'Введите исходную ссылку',
        validators=[Length(1, 256), Optional()]
    )
    custom_id = StringField(
        'Введите короткую ссылку',
        validators=[Length(1, 128), Optional()]
    )
    submit = SubmitField('Сократить')
