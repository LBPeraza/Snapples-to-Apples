import jank_windows_fix
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', pagename="Home")

@app.route('/Login')
def login():
    return render_template('login.html')

@app.route('/Newuser')
def newuser():
    return render_template('newuser.html')

@app.route('/Existinguser')
def existinguser():
    return render_template('existinguser.html')

@app.route('/Play')
def play():
    return render_template('play.html')







if __name__ == '__main__':
    app.run(debug=True)
