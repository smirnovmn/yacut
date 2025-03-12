import random
import string

from . import db
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


def is_url_exists(url):
    if URLMap.query.filter_by(short=url).first() is not None:
        return True
    return False