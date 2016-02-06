from app import db
from sqlalchemy.ext.hybrid import hybrid_property
import hashlib

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    _password = db.Column(db.String(128), nullable=False)
    experience = db.Column(db.Integer, default=0)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        m = hashlib.sha512()
        m.update(plaintext.encode())
        self._password = m.digest()

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.experience = 0

    def is_correct_password(self, plaintext):
        m = hashlib.sha512()
        m.update(plaintext.encode())
        return m.digest() == self.password

    def __repr__(self):
        return '<User %s>' % self.username

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phrase = db.Column(db.String(50))
    users = db.relationship(
        'User',
        backref=db.backref('game', lazy='joined'),
        lazy='dynamic'
    )
    host_id = db.Column(db.Integer, nullable=False)
    order_seed = db.Column(db.Integer, default=0)
    rounds = db.Column(db.Integer, default=3)
    current_round = db.Column(db.Integer, default=0)
    current_player = db.Column(db.Integer)
    pictures = db.relationship(
        'Picture',
        backref=db.backref('game', lazy='joined'),
        lazy='dynamic'
    )
    in_progress = db.Column(db.Boolean, default=False)


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    data = db.Column(db.LargeBinary)
