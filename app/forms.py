from flask_wtf import Form
from wtforms import BooleanField, TextField, PasswordField, validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask.ext.uploads import UploadSet, IMAGES

images = UploadSet('images', IMAGES)

class PictureForm(Form):
    picture = FileField('picture', [
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