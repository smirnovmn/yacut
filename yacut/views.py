import os

from flask import abort, flash, redirect, render_template

from . import app
from .constans import LENGTH_SHORT_LINK
from .forms import UrlMapForm
from .models import URLMap
from .utils import (entry_db, get_unique_short_id, is_url_exists,
                    is_valid_shortlink)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlMapForm()
    if form.validate_on_submit():
        if form.custom_id.data and is_valid_shortlink(form.custom_id.data):
            custom_id = form.custom_id.data
        else:
            custom_id = get_unique_short_id(LENGTH_SHORT_LINK)
        if is_url_exists(custom_id):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        urlmap = entry_db(form.original_link.data, custom_id)
        return render_template(
            'index.html',
            form=form,
            short_url=os.getenv('BASE_URL', default='http://localhost/') + urlmap.short,
            original_link=urlmap.original
        )
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_to_original(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        return abort(404)
    return redirect(urlmap.original)
