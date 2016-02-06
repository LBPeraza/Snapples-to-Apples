from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    experience = db.Column(db.Integer, default=0)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phrase = db.Column(db.String(50))
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'), nullable=False)
    users = db.relationship('User', backref='game', lazy='dynamic')
    order_seed = db.Column(db.Integer, default=0)
    rounds = db.Column(db.Integer, default=3)
    current_round = db.Column(db.Integer, default=0)
    current_player = db.Column(db.Integer)
    pictures = db.relationship('Picture', backref='game', lazy='dynamic')


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    data = db.Column(db.LargeBinary)
