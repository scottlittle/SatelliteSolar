from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def zack_rules():
    content = ''
    for i in xrange(1000):
        content += 'zack rules! '
    return '<h1> Yo: %s </h1>' % content


@app.route('/rainbow_rules')
def rainbow_rules():
    colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#8F00FF']
    mydivs = ''
    myhtml = ''
    element = ''
    basecode = """
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>title</title>
        </head>

      <body>
        <!-- page content -->
        %s
      </body>

    </html>
    """

    for i in xrange(33):
        color_index = i % 6
        element += """ <div style="background-color: %s; color: white; text-align: center;">
            yolo
        </div>
        """ % (colors[color_index])

    return basecode % element

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)




# @app.route('/rainbow_rules')
# def rainbow_rules():
#     colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#8F00FF']
#     mydivs = ''
#     for i in xrange(33):
#         color_index = i % 6
#         element = '<div style="background-color: %s;"> yolo </div>' % colors[color_index]
#         mydivs += element
#         mydivs += '\n'
#     return mydivs
