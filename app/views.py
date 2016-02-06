from flask import Blueprint, render_template, abort, flash

from app.models import *
from app.helpers import *

mod = Blueprint('snapples',
                __name__,
                url_prefix='/',
                static_folder='static')


@mod.route('/')
def index():
    if isLoggedIn():
        return render_template('user-index.html')
    else:
        return render_template('index.html')


@mod.route('upload/', methods=['GET', 'POST'])
@loginRequired
def uploadPicture():
    return redirect(url_for('.index'))


@mod.route('view/<picID>', methods=['GET'])
@loginRequired
def viewPicture(picID):
    if not picID.isdigit():
        abort(404)
    picture = Picture.query.filter_by(id=int(picID))
    if not picture:
        abort(404)
    return picture.data


if __name__ == '__main__':
    app.run(debug=True)
