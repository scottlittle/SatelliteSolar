from flask import Flask
from flask import request
app = Flask(__name__)
from flask import render_template
from StringIO import StringIO

# Form page to submit text
#============================================
# create page with a form on it
@app.route('/', methods=['POST','GET'])
def submission_page():
    return render_template('template.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/output', methods=['POST','GET'] )
def output():

    panel_type_data = request.form['panel_type']
    number_panels_data = int(request.form['number_panels'])
    month_data = int(request.form['month'])
    day_data = int(request.form['day'])
    hour_data = int(request.form['hour'])
    
    predicted_power = number_panels_data * 180.0

    from datetime import datetime, timedelta, time
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from data_helper_functions_webapp import find_filename, return_satellite_data

    desired_channel = 'BAND_01'
    desired_date = datetime(2014, month_data, day_data)
    desired_timedelta = timedelta(hours = hour_data)
    desired_datetime = desired_date + desired_timedelta
    satellite_filefolder = '../../data/satellite/colorado/summer6months/data/'
    sensor_filefolder = '../../data/sensor_data/colorado6months/'
    pvoutput_filefolder = '../../data/pvoutput/pvoutput6months/'

    #satellite data
    satellite_filename = find_filename(desired_datetime, desired_channel, satellite_filefolder)
    lons, lats, data = return_satellite_data(satellite_filename, satellite_filefolder)

    ##img1 = StringIO() #virtual file object
    plt.figure(figsize=(8, 8))
    imgplot = plt.imshow(data)
    imgplot.set_interpolation('none')
    plt.savefig('static/images/foo.png', bbox_inches='tight')
    
    return render_template('output.html', panel_type_data=panel_type_data, 
                           number_panels_data=number_panels_data, month_data=month_data, 
                           day_data=day_data, hour_data=hour_data, 
                           predicted_power=predicted_power)

@app.route('/get_image', methods=['POST','GET'] )
def get_image():

    # get data from request form, the key is the name you set in your form
    
    panel_type_data = request.form['panel_type']
    number_panels_data = int(request.form['number_panels'])
    month_data = int(request.form['month'])
    day_data = int(request.form['day'])
    hour_data = int(request.form['hour'])
    
    predicted_power = number_panels_data * 180.0

    from datetime import datetime, timedelta, time
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from data_helper_functions_webapp import find_filename, return_satellite_data

    desired_channel = 'BAND_01'
    desired_date = datetime(2014, month_data, day_data)
    desired_timedelta = timedelta(hours = hour_data)
    desired_datetime = desired_date + desired_timedelta
    satellite_filefolder = '../../data/satellite/colorado/summer6months/data/'
    sensor_filefolder = '../../data/sensor_data/colorado6months/'
    pvoutput_filefolder = '../../data/pvoutput/pvoutput6months/'

    #satellite data
    satellite_filename = find_filename(desired_datetime, desired_channel, satellite_filefolder)
    lons, lats, data = return_satellite_data(satellite_filename, satellite_filefolder)

    ##img1 = StringIO() #virtual file object
    plt.figure(figsize=(8, 8))
    imgplot = plt.imshow(data)
    imgplot.set_interpolation('none')
    plt.savefig('static/images/foo.png', bbox_inches='tight')
    return send_file('static/images/foo.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)