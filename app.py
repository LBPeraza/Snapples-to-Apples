import jank_windows_fix
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', pagename='Home')


if __name__ == '__main__':
    app.run(debug=True)
