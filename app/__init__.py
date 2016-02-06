from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

@app.errorhandler(404)
def notFound(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(501)
def notImplemented(error):
    return render_template('errors/501.html'), 501

from app.views import mod
app.register_blueprint(mod)

if __name__ == '__main__':
    app.run(debug=True)
