import random
import string

from flask import flash

from . import db
from .constans import LENGTH_SHORT_LINK
from .error_handlers import InvalidAPIUsage
from .models import URLMap

valid_symbols = (string.ascii_letters + string.digits)


def is_valid_shortlink(shortlink):
    if len(shortlink) < 16:
        for letter in shortlink:
            if letter not in valid_symbols:
                return False
        return True
    return False


def entry_db(original_link, custom_link):
    urlmap = URLMap(
        original=original_link,
        short=custom_link,
    )
    db.session.add(urlmap)
    db.session.commit()
    return urlmap


def get_unique_short_id(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def is_url_exists(short=None, original=None):
    if original is not None:
        if URLMap.query.filter_by(original=original).first() is not None:
            return True
    if short is not None:
        if URLMap.query.filter_by(short=short).first() is not None:
            return True
    return False


def create_shortlink_api(original, short=None):
    if not original:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if is_url_exists(original=original):
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    if not short:
        short_link = get_unique_short_id(LENGTH_SHORT_LINK)
    elif not is_valid_shortlink(short):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    else:
        short_link = short
    return entry_db(original, short_link)


def create_shortlink_interface(original, short=None, form=None):
    if short and is_valid_shortlink(short):
        custom_id = short
    else:
        custom_id = get_unique_short_id(LENGTH_SHORT_LINK)
    if is_url_exists(short=custom_id):
        flash('Предложенный вариант короткой ссылки уже существует.')
        return None
    return entry_db(original, custom_id)