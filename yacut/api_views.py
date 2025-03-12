import os

from flask import jsonify, request
from werkzeug.exceptions import BadRequest

from . import app
from .constans import LENGTH_SHORT_LINK
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import entry_db, get_unique_short_id, is_valid_shortlink


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    try:
        data = request.get_json()
    except BadRequest:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if not data.get('url'):
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if URLMap.query.filter_by(original=data['url']).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    custom_id = data.get('custom_id')
    if not custom_id:
        short_link = get_unique_short_id(LENGTH_SHORT_LINK)
    elif not is_valid_shortlink(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    else:
        short_link = custom_id
    urlmap = entry_db(data['url'], short_link)
    return jsonify({
        'short_link': os.getenv('BASE_URL') + urlmap.short,
        'url': urlmap.original
    }), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200
