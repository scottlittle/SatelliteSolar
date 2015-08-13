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
        This is where text can live or pics or go anything your little heart wishes to be done.
    </div>
  </body>

</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)