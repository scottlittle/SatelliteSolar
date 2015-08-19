from flask import Flask
from flask import request
app = Flask(__name__)
from flask import render_template
from solarApp_helper_functions import return_power
from sklearn.externals import joblib #joblib is sklearn's pickle

#load models when app starts
sat_to_sensor_model = joblib.load('models/sat-to-sensor-model/sat-to-sensor-model.pkl')
sensor_to_power_mod = joblib.load('models/sensor-to-power-model/sensor-to-power-model.pkl')

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
    predicted_power = return_power(month_data, day_data, hour_data, 
                                   sat_to_sensor_model, sensor_to_power_mod) \
                        / 66.0 * number_panels_data
    
    
    render_template('output.html', panel_type_data=panel_type_data, 
                           number_panels_data=number_panels_data, month_data=month_data, 
                           day_data=day_data, hour_data=hour_data, 
                           predicted_power=int(predicted_power))
    
    return render_template('output.html', panel_type_data=panel_type_data, 
                           number_panels_data=number_panels_data, month_data=month_data, 
                           day_data=day_data, hour_data=hour_data, 
                           predicted_power=int(predicted_power))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)