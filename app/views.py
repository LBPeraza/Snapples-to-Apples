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
        return loggedInPage()
    else:
        return render_template('index.html')


def loggedInPage():
    info = session.get('user-info')
    user = User.query.filter_by(id=info['id']).first()
    assert(user is not None)
    game = user.game
    if game is None:
        games = []
        for g in Game.query.filter_by(in_progress=False):
            thisGame = {}
            host = User.query.filter_by(id=g.host_id).first()
            thisGame['id'] = g.id
            thisGame['host'] = host.username
            thisGame['playercount'] = g.users.count()
            games.append(thisGame)
        return render_template('user-index.html', pagename='Home', games=games)
    else:
        abort(501)

@mod.route('login/', methods=['GET', 'POST'])
def login():
    if session.get('info') is not None:
        flash('You\'re already logged in!', 'warning')
        return redirect(url_for('.index'))
    form = UsernamePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        #try to log them in
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('User not found', 'danger')
        elif user.is_correct_password(form.password.data):
            #log in the user
            userInfo = dict()
            userInfo['username'] = user.username
            userInfo['id'] = user.id
            session['user-info'] = userInfo
            return redirect(url_for('.index'))
        else:
            flash('Password incorrect', 'danger')
            flashErrors(form)
    return render_template('login.html', form=form)
    
@mod.route('register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        #register them
        user = User(form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering!', 'success')
        return redirect(url_for('.index'))
    flashErrors(form)
    return render_template('register.html', form=form)


@mod.route('join/<gameID>', methods=['GET'])
@loginRequired
def joinGame(gameID):
    game = Game.query.filter_by(id=gameID).first()
    if game is None:
        flash('That game (%d) doesn\'t exist!' % gameID, 'danger')
        return redirect(url_for('.index'))
    user = User.query.filter_by(id=session['user-info']['id']).first()
    if user.game is not None:
        flash('You\'re already in a game!', 'warning')
        return redirect(url_for('.index'))
    user.game = game
    db.session.commit()
    return redirect(url_for('.index'))


@mod.route('upload/', methods=['GET', 'POST'])
@loginRequired
def uploadPicture():
    form = PictureForm()
    if form.validate_on_submit():
        picture = Picture()
        picture.data = form.picture.data.read()
        db.session.add(picture)
        db.session.commit()
        flash('Success! Picture id: %d' % picture.id, 'success')
        return redirect(url_for('.index'))
    else:
        flashErrors(form)
        return render_template('upload.html', form=form)


@mod.route('view/<picID>', methods=['GET'])
@loginRequired
@nocache
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


if __name__ == '__main__':
    app.run(debug=True)
