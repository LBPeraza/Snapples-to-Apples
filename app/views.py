from flask import Blueprint, render_template

from app.models import *

mod = Blueprint('snapples', __name__, url_prefix='/', static_folder='static')


@mod.route('/')
def index():
    return render_template('index.html', pagename='Home')


if __name__ == '__main__':
    app.run(debug=True)
