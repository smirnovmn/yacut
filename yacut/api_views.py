import os

from flask import jsonify, request
from werkzeug.exceptions import BadRequest

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import create_shortlink_api


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    try:
        data = request.get_json()
    except BadRequest:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    urlmap = create_shortlink_api(data.get('url'), data.get('custom_id'))
    return jsonify({
        'short_link': os.getenv(
            'BASE_URL', default='http://localhost/'
        ) + urlmap.short,
        'url': urlmap.original
    }), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200
