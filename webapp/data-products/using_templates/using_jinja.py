from flask import Flask
from flask import render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('using_jinja.html')

@app.route('/super_powers')
def super_powers():
    df = pd.DataFrame( {'a': [1,2,3], 'b': [4,5,6] } )
    rng = np.random.random
    
    return render_template('super_powers.html', df = df, numpy = rng )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
