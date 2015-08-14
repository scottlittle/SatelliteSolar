# when ran, grabs all 6 channels from satellite data and stores it into file X and Y

from datetime import datetime,timedelta, time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_helper_functions import *
from IPython.display import display
pd.options.display.max_columns = 999
from __future__ import division
%matplotlib inline

#iterate over datetimes:
mytime = datetime(2014, 4, 1, 13)
times = make_time(mytime)

satellite_filefolder = 'data/satellite/colorado/summer6months/data/'
sensor_filefolder = 'data/sensor_data/colorado6months/'

X = []
Y = []

for desired_datetime in times: 
    
    try: #ignore data without satellite images, should update to output datetime of occurrance
        desired_date = (desired_datetime - timedelta(hours=6)).date() #make sure correct date
        desired_date = datetime.combine(desired_date, time.min) #get into datetime format

        desired_channel = 'BAND_01' #problems with an inner for loop (doesn't look good, but works)
        satellite_filename = find_filename(desired_datetime, desired_channel, satellite_filefolder)
        lons, lats, data1 = return_satellite_data(satellite_filename, satellite_filefolder)
        
        desired_channel = 'BAND_02'
        satellite_filename = find_filename(desired_datetime, desired_channel, satellite_filefolder)
        lons, lats, data2 = return_satellite_data(satellite_filename, satellite_filefolder)
        
        desired_channel = 'BAND_03'
        satellite_filename = find_filename(desired_datetime, desired_channel, satellite_filefolder)
        lons, lats, data3 = return_satellite_data(satellite_filename, satellite_filefolder)               

        desired_channel = 'BAND_04'
        satellite_filename = find_filename(desired_datetime, desired_channel, satellite_filefolder)
        lons, lats, data4 = return_satellite_data(satellite_filename, satellite_filefolder)
        
        desired_channel = 'BAND_06'
        satellite_filename = find_filename(desired_datetime, desired_channel, satellite_filefolder)
        lons, lats, data5 = return_satellite_data(satellite_filename, satellite_filefolder)

        sensor_filename = find_file_from_date(desired_date, sensor_filefolder)
        df_sensor = return_sensor_data(sensor_filename, sensor_filefolder).ix[:,-15:-1]
        df_sensor[df_sensor.index == desired_datetime]

        Y.append(df_sensor[df_sensor.index == desired_datetime].values[0])
        X.append(np.hstack( ( np.ravel(data1) , np.ravel(data2), np.ravel(data3) , np.ravel(data4), np.ravel(data5) ) ) )
    except:
         pass

X = np.array(X)
Y = np.array(Y)

np.savez_compressed('data/Y_all_channels.npz',Y=Y)
np.savez_compressed('data/X_all_channels.npz',X=X)

