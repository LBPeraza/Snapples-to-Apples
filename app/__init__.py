from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLALchemy(app)

@app.errorhandler(404)
def notFound(error):
    return render_template('errors/404.html'), 404

from app.views import mod
app.register_blueprint(mod)

if __name__ == '__main__':
    app.run()
