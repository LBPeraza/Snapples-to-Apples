import eventlet

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.socketio import SocketIO

from app.helpers import isLoggedIn

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

eventlet.monkey_patch()
socketio = SocketIO(app, async_mode='eventlet')

@app.errorhandler(404)
def notFound(error):
    return render_template('errors/404.html', loggedIn=isLoggedIn()), 404

@app.errorhandler(501)
def notImplemented(error):
    return render_template('errors/501.html', loggedIn=isLoggedIn()), 501

from app.views import mod
app.register_blueprint(mod)

from app.sockets import initSockets
initSockets(socketio, db)

if __name__ == '__main__':
    socketio.run(app)
