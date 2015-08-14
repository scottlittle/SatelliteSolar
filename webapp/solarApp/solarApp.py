from flask import Flask
from flask import request
app = Flask(__name__)
from flask import render_template

# Form page to submit text
#============================================
# create page with a form on it
@app.route('/', methods=['POST','GET'])
def submission_page():
    return render_template('template.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/word_counter', methods=['POST','GET'] )
def word_counter():

    # get data from request form, the key is the name you set in your form
    panel_type_data = request.form['panel_type']
    number_panels_data = request.form['number_panels']
    number_panels_data = int(number_panels_data)
    
    return render_template('template2.html', panel_type_data=panel_type_data, 
                           number_panels_data=number_panels_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)