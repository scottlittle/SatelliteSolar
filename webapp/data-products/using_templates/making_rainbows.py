from flask import Flask
from flask import render_template
import pandas as pd
app = Flask(__name__)


@app.route('/')
def hello_world():
    colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#8F00FF']
    return render_template('making_rainbows.html', colors = colors)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
