from flask.ext.socketio import emit, join_room, leave_room

from app.models import *
from app.helpers import *


def initSockets(socketio, db):
    @socketio.on('connect')
    @socketLoginRequired
    def connect():
        join_room(session['user-info']['username'])

    
    @socketio.on('disconnect')
    @socketLoginRequired
    def disconnect():
        leave_room(session['user-info']['username'])
