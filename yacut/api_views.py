import re
from flask import jsonify, request

from . import app, db
from .constans import BASE_URL
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id
from .utils import check


# @app.route('/api/id/', methods=['POST'])
# def add():
#     data = request.get_json()
#     if not data:
#         raise InvalidAPIUsage('Отсутствует тело запроса')
#     if not data.get('url'):
#         raise InvalidAPIUsage('"url" является обязательным полем!')
#     if URLMap.query.filter_by(original=data['url']).first() is not None:
#         raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
#     custom_id = data.get('custom_id')
#     if not custom_id:
#         short_link = get_unique_short_id(6)
#     elif not check(custom_id):
#         raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
#     else:
#         short_link = custom_id
#     urlmap = URLMap(
#         original=data['url'],
#         short=short_link,
#     )
#     db.session.add(urlmap)
#     db.session.commit()
#     return jsonify({
#         'url': data['url'],
#         'short_link': BASE_URL + short_link
#     }), 201


@app.route('/api/id/', methods=['POST'])
def add():
    try:
        data = request.get_json()
    except:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if not data.get('url'):
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if URLMap.query.filter_by(original=data['url']).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    custom_id = data.get('custom_id')
    if not custom_id:
        short_link = get_unique_short_id(6)
    elif not check(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    else:
        short_link = custom_id
    urlmap = URLMap(
        original=data['url'],
        short=short_link,
    )
    db.session.add(urlmap)
    db.session.commit()
    return jsonify({
        'url': data['url'],
        'short_link': BASE_URL + short_link
    }), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200