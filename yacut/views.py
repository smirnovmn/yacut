import random
import string
from random import randrange

from flask import abort, flash, redirect, render_template

from . import app, db
from .constans import BASE_URL
from .forms import UrlMapForm
from .models import URLMap
from .utils import check


def get_unique_short_id(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlMapForm()
    if form.validate_on_submit():
        if form.custom_id.data and check(form.custom_id.data):
            custom_id = form.custom_id.data
        else:
            custom_id = get_unique_short_id(6)
        urlmap = URLMap(
            original=form.original_link.data,
            short=custom_id,
        )
        if URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        db.session.add(urlmap)
        db.session.commit()

        return render_template(
            'index.html',
            form=form,
            short_url=BASE_URL + urlmap.short,
            original_link=urlmap.original
        )
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_to_original(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        return abort(404)
    return redirect(urlmap.original)
