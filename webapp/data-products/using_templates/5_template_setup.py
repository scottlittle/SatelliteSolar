from flask import Flask
from flask import render_template
import pandas as pd
app = Flask(__name__)

@app.route('/')
def hello_world():
    df = pd.read_csv('some.csv')
    df = df.set_index('Unnamed: 0')
    px = df['px'].values
    years = df['year'].values
    mydata = zip(px,years)
    return render_template('passing_variables_into_html.html', data=mydata )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
