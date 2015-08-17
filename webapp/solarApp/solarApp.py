from flask import Flask
from flask import request
app = Flask(__name__)
from flask import render_template
from StringIO import StringIO
from solarApp_helper_functions import return_power

@app.route('/', methods=['POST','GET'])
def submission_page():
    return render_template('template.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/output', methods=['POST','GET'] )
def output():
    
    #form data
    panel_type_data = request.form['panel_type']
    number_panels_data = int(request.form['number_panels'])
    month_data = int(request.form['month'])
    day_data = int(request.form['day'])
    hour_data = int(request.form['hour'])
    
    #pred power calculation and getting satellite image into foo.png
    predicted_power = return_power(month_data, day_data, hour_data) / 66.0 * number_panels_data
    
    return render_template('output.html', panel_type_data=panel_type_data, 
                           number_panels_data=number_panels_data, month_data=month_data, 
                           day_data=day_data, hour_data=hour_data, 
                           predicted_power=int(predicted_power))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)