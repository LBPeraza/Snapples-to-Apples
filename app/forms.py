from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
# from wtforms.validators import FileRequired, FileAllowed
from flask.ext.uploads import UploadSet, IMAGES

images = UploadSet('images', IMAGES)

class PictureForm(Form):
    picture = FileField('picture', [
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Just Images!')
    ])
