from flask import Flask
from flask import request
app = Flask(__name__)
from flask import render_template

# Form page to submit text
#============================================
# create page with a form on it
@app.route('/')
def submission_page():
    #content = 'hello'
    return render_template('template.html')

@app.route('/about')
def about_page():
    #content = 'hello'
    return render_template('about.html')

@app.route('/word_counter', methods=['POST','GET'] )
def word_counter():
#     if request.method == 'POST':
#         return ''
    # get data from request form, the key is the name you set in your form
    data = request.form['user_input']

    # convert data to list
    data = [data]

    import pickle
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    

    for doc, category in zip(data, predicted):
        #return('%r => %s' % (doc, categories[category]))
        return render_template('template2.html', doc=doc, category=categories[category])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)