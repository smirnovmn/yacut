import os

from flask import abort, redirect, render_template

from . import app
from .forms import UrlMapForm
from .models import URLMap
from .utils import create_shortlink_interface


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlMapForm()
    if form.validate_on_submit():
        urlmap = create_shortlink_interface(
            form.original_link.data, form.custom_id.data, form
        )
        if not urlmap:
            return render_template('index.html', form=form)
        return render_template(
            'index.html',
            form=form,
            short_url=os.getenv(
                'BASE_URL', default='http://localhost/'
            ) + urlmap.short,
            original_link=urlmap.original
        )
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_to_original(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        return abort(404)
    return redirect(urlmap.original)
