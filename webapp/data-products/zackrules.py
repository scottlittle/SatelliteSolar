from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def index():
    #assert 0
    return '<h1> Something </h1>'

# adding a new page
@app.route('/zack_rules')
def zack_rules():
    content = ''
    # generate some content
    for i in xrange(1000):
        content += 'zack rules! '
    return render_template('template.html', content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085, debug=True)