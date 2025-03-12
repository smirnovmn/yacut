from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields import StringField
from wtforms.validators import Optional

from .constans import CUSTOM_ID_RANGE, ORIGINAL_LINK_RANGE


class UrlMapForm(FlaskForm):
    original_link = StringField(
        'Введите исходную ссылку',
        validators=[ORIGINAL_LINK_RANGE, Optional()]
    )
    custom_id = StringField(
        'Введите короткую ссылку',
        validators=[CUSTOM_ID_RANGE, Optional()]
    )
    submit = SubmitField('Сократить')
