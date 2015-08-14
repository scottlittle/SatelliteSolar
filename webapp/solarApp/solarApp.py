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
    number_panels_data = int(request.form['number_panels'])
    month_data = int(request.form['month'])
    hour_data = int(request.form['hour'])
    
    if panel_type_data == 'Solyndra':
        predicted_power = 0
    else:
        predicted_power = number_panels_data * 180.0
    
    return render_template('template2.html', panel_type_data=panel_type_data, 
                           number_panels_data=number_panels_data, month_data=month_data, 
                          hour_data=hour_data, predicted_power=predicted_power)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)