import numpy as np
import pandas as pd
from flask import Flask
from flask import request, render_template, jsonify, Response
import json
#import ipdb
app = Flask(__name__)


# Form page to submit text
#============================================
# create page with a form on it
@app.route('/')
def plot_page():
    return render_template('vega.html')



# 
# Data plotting app.
#
@app.route('/get_data')
def get_data():
    df = pd.DataFrame({'x':range(10), 'y':np.random.rand(10),
                       'c':0})
    #Return this in the way vega wants it.
    return Response(json.dumps(df.T.to_dict().values()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
