from wtforms import Form, BooleanField, TextField, PasswordField, validators

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [validators.Required(), 
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

class UsernamePasswordForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])