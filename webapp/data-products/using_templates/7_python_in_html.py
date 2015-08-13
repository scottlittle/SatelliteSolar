from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('python_in_html.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
