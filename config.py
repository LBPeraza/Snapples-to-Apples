import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'shhh, don\'t tell anyone'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'db.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True
