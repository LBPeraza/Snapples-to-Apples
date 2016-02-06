from flask import Blueprint, render_template, abort, flash, request

from app.models import *
from app.helpers import *
from app.forms import *

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

@mod.route('login/', methods=['GET', 'POST'])
def login():
    form = UsernamePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        #try to log them in
        user = User.query.filter_by(username==form.username.data).first_or_404()
        if user.is_correct_password(form.password.data):
            #log in the user
            userInfo = dict()
            userInfo['username'] = user.username
            userInfo['id'] = user.id
            db_session['user-info'] = userInfo
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', form=form)
    
@mod.route('register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        #register them
        user = User(form.username.data, form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

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
