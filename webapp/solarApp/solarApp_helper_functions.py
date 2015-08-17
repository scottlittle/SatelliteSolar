from __future__ import division
from scipy.ndimage import zoom
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta, time
from data_helper_functions_webapp import *
from time import sleep

def return_power(month_data, day_data, hour_data):
    '''Input: datetime
    Output: power
    Info: also makes satellite image'''

    ######### Satellite image ###############
    # get sat image first, so it may be redered by computation is done
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

    plt.figure(figsize=(8, 8))
    imgplot = plt.imshow(data)
    imgplot.set_interpolation('none')
    plt.savefig('static/images/foo.png', bbox_inches='tight') # save sat image to foo.png

    ############## Model for satellite to sensor ############################

    X = [] #sat data
    Y = [] #sensor data

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

    X,Y = (np.array(X),np.array(Y))

    ####################### Make sat data useful ####################
    X_ratio_1_2 = []
    for i in xrange(X.shape[0]): #a little awkward since X is only one row, but no need to change
        CH1 = zoom(X[:,0:1972][i].reshape((29,68)),zoom=(0.48, 0.53), order=5)
        CH2 = X[:,1972:2476][i].reshape((14,36))
        X_ratio_1_2.append(25000* (CH2)  / (CH1 + CH2+1.0) )
    X_ratio_1_2 = np.array(X_ratio_1_2)

    X_ratio_1_6 = []
    for i in xrange(X.shape[0]):
        CH1 = zoom(X[:,0:1972][i].reshape((29,68)),zoom=(0.48, 0.53), order=5)
        CH6 = X[:,3484:3988][i].reshape((14,36))
        X_ratio_1_6.append(25000* CH6 / (CH1 + CH6 + 0.1) )
    X_ratio_1_6 = np.array(X_ratio_1_6)

    X_ratio_2_6 = []
    for i in xrange(X.shape[0]):
        CH2 = X[:,1972:2476][i].reshape((14,36))
        CH6 = X[:,3484:3988][i].reshape((14,36))
        X_ratio_2_6.append(25000* CH6 / (CH2 + CH6 + 0.1) )
    X_ratio_2_6 = np.array(X_ratio_2_6)

    ######## change X into histogram #############
    X_hist = []
    bins = 25
    for i in xrange(X.shape[0]):
        myval1 = pd.DataFrame(np.ravel(X_ratio_1_2[i])).fillna(np.mean).values.flatten();
        myval2 = pd.DataFrame(np.ravel(X_ratio_1_6[i])).fillna(np.mean).values.flatten();
        myval3 = pd.DataFrame(np.ravel(X_ratio_2_6[i])).fillna(np.mean).values.flatten();

        hist1, _ = np.histogram(X[:,0:1972][i], density=True, bins=bins, range=(0,25000))
        hist2, _ = np.histogram(X[:,1972:2476][i], density=True, bins=bins, range=(0,25000))
        hist3, _ = np.histogram(X[:,2476:2980][i], density=True, bins=bins, range=(0,25000))
        hist4, _ = np.histogram(X[:,2980:3484][i], density=True, bins=bins, range=(0,25000))
        hist5, _ = np.histogram(X[:,3484:3988][i], density=True, bins=bins, range=(0,25000))
        hist6, _ = np.histogram( myval1 , density=True, bins=bins, range=(0,25000) )
        hist7, _ = np.histogram( myval2 , density=True, bins=bins, range=(0,25000))
        hist8, _ = np.histogram( myval3, density=True, bins=bins, range=(0,25000))
        X_hist.append(np.hstack((hist1,hist2,hist3,hist4,hist5,hist6,hist7,hist8)))

    X_hist = np.array(X_hist)

    #################### Import models #######################

    from sklearn.externals import joblib #joblib is sklearn's pickle
    sat_to_sensor_model = joblib.load('models/sat-to-sensor-model/sat-to-sensor-model.pkl')
    sensor_to_power_mod = joblib.load('models/sensor-to-power-model/sensor-to-power-model.pkl')

    X_sensor = sat_to_sensor_model.predict(X_hist)
    y_power = sensor_to_power_mod.predict(X_sensor)

    return y_power[0]


