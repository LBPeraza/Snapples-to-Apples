from flask_wtf import Form
from wtforms import (BooleanField, TextField, PasswordField, validators,
                     IntegerField)
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask.ext.uploads import UploadSet, IMAGES

images = UploadSet('images', IMAGES)

class PictureForm(Form):
    picture = FileField('Your picture', [
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Just Images!')
    ])

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
