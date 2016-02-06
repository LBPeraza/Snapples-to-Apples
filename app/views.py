<<<<<<< HEAD
import io
from flask import Blueprint, render_template, abort, flash, send_file, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import ADMINS
from app import app, db
from app.models import *
from app.helpers import *
from app.forms import *

mod = Blueprint('snapples',
                __name__,
                url_prefix='/',
                static_folder='static')

admin = Admin(app)
class AuthAdminView(ModelView):
    def __init__(self, view):
        super().__init__(view, db.session)

    def is_accessible(self):
        return True
        info = session.get('info')
        if info is None:
            return False
        else:
            return info['username'] in 'ADMINS'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('.index'))

admin.add_view(AuthAdminView(User))
admin.add_view(AuthAdminView(Game))
admin.add_view(AuthAdminView(Picture))


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
    form = PictureForm()
    if form.validate_on_submit():
        picture = Picture()
        picture.data = form.picture.data.read()
        db.session.add(picture)
        db.session.commit()
        flash('Success!')
        return redirect(url_for('.index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print("Error in %s -- %s" % (getattr(form,field).label.text, error))
        return render_template('upload.html', form=form)


@mod.route('view/<picID>', methods=['GET'])
@loginRequired
def viewPicture(picID):
    if not picID.isdigit():
        abort(404)
    picture = Picture.query.filter_by(id=int(picID)).first()
    if not picture:
        abort(404)
    print(len(picture.data))
    return send_file(io.BytesIO(picture.data))

@mod.route('logout/')
def logout():
    session.clear()
    return redirect(url_for('.index'))


@mod.route('fakelogin/')
def fakeLogin():
    session['user-info'] = {
        'name': 'jdoe',
        'id': -1
    }
    return redirect(url_for('.index'))


if __name__ == '__main__':
    app.run(debug=True)
