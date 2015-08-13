from flask import Flask
from flask import request
app = Flask(__name__)

# OUR HOME PAGE
#============================================
@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>title</title>
    </head>

  <body>
    <!-- page content -->
    <div>
        This is where text or pics or anything your little heart wishes can go.
    </div>
  </body>

</html>
'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
