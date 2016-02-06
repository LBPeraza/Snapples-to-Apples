import io
import random
import time

from flask import Blueprint, render_template, abort, flash, send_file, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import ADMINS
from app import app, db, socketio
from app.models import *
from app.helpers import *
from app.forms import *

adjs = initializeAdjDict()

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


@mod.route('/', methods=['GET', 'POST'])
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
        return render_template('user-index.html',
                               pagename='Home',
                               games=games,
                               form=GameForm())
    else:
        return gamePage(user, game)


def gamePage(user, game):
    if game.in_progress:
        return gamePlay(user, game)
    else:
        users = getPlayerOrder(game)
        form = GameForm()
        return render_template('game-lobby.html',
                               username=session['user-info']['username'],
                               users=users,
                               isHost=game.host_id == user.id,
                               form=form)

def gamePlay(user, game):
    if game.current_round > game.rounds: #game is over
        return gameOver(user, game)
    elif game.phrase == "" or game.phrase == None:
        return pickingPhase(user, game)
    else:
        picker_id = game.current_player
        if picker_id == user.id:
            return selectingPhase(user, game)
        else:
            return uploadingPhase(user, game)

def myKey(user):
    return user.experience

def gameOver(user, game):
    form = GameOverForm(request.form)
    users = game.users
    users = sorted(users, key=myKey)
    game.in_progress = False
    db.session.commit()
    return render_template('gameOver.html', form=form, users=game.users)

def pickingPhase(user, game):
    form = PickAWordForm(request.form)
    words = getWord(adjs, 5)
    picker_id = game.current_player
    picker = User.query.filter_by(id=picker_id).first()
    return render_template('pickaword.html', form=form, 
        isPicker=picker_id == user.id, words=words, picker=picker.username,
        game_round=game.current_round)

def selectingPhase(user, game):
    form = PlayGameForm(request.form)
    return render_template('playGame.html', form=form, word=game.phrase,
        round=game.current_round, pictures=game.pictures)

def uploadingPhase(user, game):
    picture = Picture.query.filter_by(user_id=user.id).first()
    picker_id = game.current_player
    picker = User.query.filter_by(id=picker_id).first()
    if picture == None:
        form = TakeForm(request.form)
        return render_template('take.html', form=form, word=game.phrase,
            round=game.current_round, picker=picker.username)
    else:
        form = WaitForm(request.form)
        return render_template('wait.html', picker=picker.username, 
            picture=picture.id, round=game.current_round,
            word=game.phrase)


@mod.route('beginGame/', methods=['GET', 'POST'])
@loginRequired
def beginGame():
    user = User.query.filter_by(id=session['user-info']['id']).first()
    assert(user is not None)
    game = user.game
    if game is None:
        flash('You\'re not in a game', 'warning')
        return redirect(url_for('.index'))
    game.in_progress = True
    game.current_round = 0
    users = getPlayerOrder(game)
    game.current_player = users[0].id
    db.session.commit()
    return redirect(url_for('.index'))

@mod.route('pick/<word>', methods=['GET'])
@loginRequired
def pick(word):
    user = User.query.filter_by(id=session['user-info']['id']).first()
    game = user.game
    if game is None:
        flash('You\'re not in a game!', 'warning')
        return redirect(url_for('.index'))
    game.phrase = word
    db.session.commit()
    return redirect(url_for('.index'))

@mod.route('take/', methods=['GET', 'POST'])
@loginRequired
def take():
    form = PictureForm()
    if request.method == 'POST' and form.validate():
        #get the picture and do stuff with it
        user = User.query.filter_by(id=session['user-info']['id']).first()
        game = user.game
        if game is None:
            flash('You\'re not in a game!', 'warning')
            return redirect(url_for('.index'))
        picture = Picture()
        picture.data = form.picture.data.read()
        picture.user_id = session['user-info']['id']
        db.session.add(picture)
        game.pictures.append(picture)
        db.session.commit()
        return 'Success'
    flashErrors(form)
    return render_template('take.html', form=form)

@mod.route('winner/<picture>', methods=['GET'])
@loginRequired
def winner(picture):
    user = User.query.filter_by(id=session['user-info']['id']).first()
    game = user.game
    if game is None:
        flash('You\'re not in a game!', 'warning')
        return redirect(url_for('.index'))
    if game.current_player != user.id:
        flash('You\'re not the current picker!', 'warning')
        return redirect(url_for('.index'))
    game.current_round += 1
    pic = Picture.query.filter_by(id=picture).first()
    playerWinner = game.users.filter_by(id=pic.user_id).first()
    playerWinner.current_streak += 1
    playerWinner.experience += playerWinner.current_streak
    playerWinner.best_streak = max(playerWinner.current_streak,
            playerWinner.best_streak)
    for player in game.users:
        if player != playerWinner and player != user:
            player.current_streak = 0

    if game.current_round <= game.rounds:
        #go on to next round
        game.phrase = ""
        for picture in game.pictures:
            picture.game_id = None
            db.session.delete(picture)
        users = getPlayerOrder(game)
        game.current_player = users[game.current_round % len(users)].id
    flash('%s was the winner!' % playerWinner.username, 'success')
    db.session.commit()
    return redirect(url_for('.index'))


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
        userinfo = {}
        userinfo['id'] = user.id
        userinfo['username'] = user.username
        session['user-info'] = userinfo
        return redirect(url_for('.index'))
    flashErrors(form)
    return render_template('register.html', form=form)


@mod.route('create', methods=['GET', 'POST'])
@loginRequired
def createGame():
    form = GameForm()
    if request.method == 'POST' and form.validate_on_submit():
        game = Game()
        game.max_players = form.maxPlayers.data
        id = session['user-info']['id']
        game.host_id = id
        host = User.query.filter_by(id=id).first()
        game.users.append(host)
        random.seed(time.time())
        game.order_seed = random.randint(-0xffffffff, 0xffffffff)
        game.rounds = form.numRounds.data
        db.session.add(game)
        db.session.commit()
        return redirect(url_for('.index'))
    flashErrors(form)
    return render_template('create.html', form=form)


@mod.route('join/<gameID>', methods=['GET'])
@loginRequired
def joinGame(gameID):
    game = Game.query.filter_by(id=gameID).first()
    if game is None:
        flash('That game (%s) doesn\'t exist!' % gameID, 'danger')
        return redirect(url_for('.index'))
    user = User.query.filter_by(id=session['user-info']['id']).first()
    if user.game is not None:
        flash('You\'re already in a game!', 'warning')
        return redirect(url_for('.index'))
    for other in game.users.all():
        socketio.emit('player joined', room=other.username)
    user.game = game
    db.session.commit()
    return redirect(url_for('.index'))


@mod.route('leave/', methods=['GET'])
@loginRequired
def leaveGame():
    user = User.query.filter_by(id=session['user-info']['id']).first()
    if user.game is None:
        flash('You aren\'t in a game!', 'warning')
        return redirect(url_for('.index'))
    user.game = None
    db.session.commit()
    return redirect(url_for('.index'))


@mod.route('kick/<id>', methods=['GET'])
@loginRequired
def kick(id):
    user = User.query.filter_by(id=session['user-info']['id']).first()
    game = user.game
    if game is None or game.host_id != user.id:
        flash('You\'re not hosting a game!', 'warning')
        return redirect(url_for('.index'))
    kickee = game.users.filter_by(id=id).first()
    if kickee:
        game.users.remove(kickee)
        socketio.emit('kicked', user.username, room=kickee.username)
        db.session.commit()
        flash('Successfully kicked %s from your match!' % kickee.username,
              'success')
    else:
        flash('That user isn\'t in your match!', 'warning')
    return redirect(url_for('.index'))


@mod.route('getKicked/<host>')
@loginRequired
def kicked(host):
    flash('You were kicked from %s\'s game!' % host, 'danger')
    return redirect(url_for('.index'))


@mod.route('makehost/<id>', methods=['GET'])
@loginRequired
def host(id):
    user = User.query.filter_by(id=session['user-info']['id']).first()
    game = user.game
    if game is None or game.host_id != user.id:
        flash('You\'re not hosting a game!', 'warning')
        return redirect(url_for('.index'))
    hostee = game.users.filter_by(id=id).first()
    if hostee:
        game.host_id = hostee.id
        db.session.commit()
        socketio.emit('made host', user.username, room=hostee.username)
        flash('Successfully made %s the host!' % hostee.username,
              'success')
    else:
        flash('That user isn\'t in your match!', 'warning')
    return redirect(url_for('.index'))


@mod.route('becomeHost/<host>', methods=['GET'])
@loginRequired
def becomeHost(host):
    flash('%s made you host of their game!' % host, 'info')
    return redirect(url_for('.index'))


@mod.route('startGame/', methods=['GET'])
@loginRequired
def startGame():
    return redirect(url_for('.index'))


@mod.route('closeGame/', methods=['GET'])
@loginRequired
def closeGame():
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
        return 'Success'
    else:
        flashErrors(form)
        return redirect(url_for('.take'))


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


@mod.route('look/<picID>', methods=['GET'])
@loginRequired
@nocache
def look(picID):
    return render_template('look.html', id=picID)


@mod.route('logout/')
def logout():
    session.clear()
    return redirect(url_for('.index'))


if __name__ == '__main__':
    app.run(debug=True)
