from flask_wtf import Form
from wtforms import (BooleanField, TextField, PasswordField, validators,
                     IntegerField, HiddenField)
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask.ext.uploads import UploadSet, IMAGES

images = UploadSet('images', IMAGES)

class WaitForm(Form):
    pass

class GameForm(Form):
    pass

class GameOverForm(Form):
    pass

class PickAWordForm(Form):
    pass

class PlayGameForm(Form):
    picture = HiddenField()

class TakeForm(Form):
    picture = HiddenField()

class PictureForm(Form):
    picture = HiddenField('picture')

class SeePictureForm(Form):
    picture = HiddenField()

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [validators.Required(), 
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

class UsernamePasswordForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

class GameForm(Form):
    maxPlayers = IntegerField('Maximum Players',
            [validators.NumberRange(min=2)])
    numRounds = IntegerField('Number of Rounds',
            [validators.Required(), validators.NumberRange(min=1)])
