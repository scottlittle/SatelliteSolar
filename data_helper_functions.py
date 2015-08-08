import netCDF4
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap  #map stuff
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from datetime import datetime, timedelta
import pandas as pd
get_ipython().magic(u'matplotlib inline')

###########
# Below are helper functions for the satellite
###########

def plot_satellite_image(filename):
	'''takes in a file and outputs a plot of satellite'''
	rootgrp = Dataset(filename, "a", format="NETCDF4")
	lons = rootgrp.variables['lon'][:]
	lats = rootgrp.variables['lat'][:]
	data = rootgrp.variables['data'][:]
	rootgrp.close() #need to close before you can open again

	# Get some parameters for the Stereographic Projection
	m = Basemap(width=800000,height=800000, #create a basemap object with these parameters
	            resolution='l',projection='stere',\
	            lat_ts=40,lat_0=39.5,lon_0=-104.5)

	xi, yi = m(lons, lats) #map onton x and y for plotting
	plt.figure(figsize=(10,10)) # Plot Data
	cs = m.pcolor(xi,yi,np.squeeze(data)) #data is 1 x 14 x 36, squeeze makes it 14 x 36

	m.drawparallels(np.arange(-80., 81., 1.), labels=[1,0,0,0], fontsize=10) # Add Grid Lines
	m.drawmeridians(np.arange(-180., 181., 1.), labels=[0,0,0,1], fontsize=10) # Add Grid Lines
	m.drawstates(linewidth=3) # Add state boundaries

	cbar = m.colorbar(cs, location='bottom', pad="10%") # Add Colorbar
	plt.title('GOES 15 - Sensor 1') # Add Title
	plt.show()

def return_satellite_data(filename, filefolder):
	''' Input:  filename
		Output: lons, lats, data'''
	rootgrp = Dataset(filefolder + filename, "a", format="NETCDF4") #generic name for data
	lons = rootgrp.variables['lon'][:] #extract lons ...
	lats = rootgrp.variables['lat'][:] #...lats...
	data = rootgrp.variables['data'][:] #...and data from netCDF file
	rootgrp.close() #need to close before you can open again
	return (lons, lats, np.squeeze(data))

def find_file_details(filefolder, filetype = 'nc'): #match 2 or 3 letters
    '''Takes in a filefolder with satellite data and returns list of files,
        list of file details, list of dates, and list of channels
        Example usage:  filefolder = "data/satellite/colorado/summer6months/data"
						list_of_files, list_of_files_details, \
						list_of_dates, list_of_channels = find_file_details(filefolder)'''

    data_files = os.listdir(filefolder) #list files in directory

    list_of_files = [] #contains all the files
    list_of_files_details = [] #contains information collected from filename
    for myfile in data_files:
        if (myfile[-2:] == filetype or myfile[-3:] == filetype): #only get netCDF by default
            list_of_files.append(myfile)
            list_of_files_details.append(myfile.split('.'))

    list_of_dates = [] #contains datetime data for files
    list_of_channels = [] #contains channel data
    for i,_ in enumerate(list_of_files_details):
        mytime = list_of_files_details[i][1]+" "+list_of_files_details[i][2]+" "+list_of_files_details[i][3]
        mydatetime = datetime.strptime(mytime, '%Y %j %H%M%S')
        list_of_dates.append(mydatetime)
        list_of_channels.append(list_of_files_details[i][4])
    return (list_of_files, list_of_files_details, list_of_dates, list_of_channels)

def find_closest_date(desired_datetime, filefolder):
	'''Input: desired datetime, Output: datetime of closest file(s)
	Example usage:   desired_datetime = datetime(2014, 5, 5, 19)
	closest_datetime = find_closest_date(desired_datetime)'''
	list_of_files, list_of_files_details, \
	list_of_dates, list_of_channels = find_file_details(filefolder)
	time_differences = []
	for i,time in enumerate(list_of_dates):
		time_difference = list_of_dates[i] - desired_datetime
		time_differences.append(abs(time_difference).total_seconds())

	if min(time_differences) < 10800: #return datetime only if < 3 hours
		return list_of_dates[np.argmin(time_differences)]
	else:
		print "No file with this datetime within 3 hours!"

def find_filename(desired_datetime, desired_channel, filefolder):
	'''return filename with desired features
	Example usage:  desired_channel = 'BAND_01'
	desired_datetime = datetime(2014, 4, 2, 12)
	print find_filename(desired_datetime, desired_channel)'''
	list_of_files, list_of_files_details, \
	list_of_dates, list_of_channels = find_file_details(filefolder)
	closest_datetime = find_closest_date(desired_datetime, filefolder)
	list_of_channel_matches = []
	for i,channel in enumerate(list_of_channels):
		if channel == desired_channel:
			list_of_channel_matches.append(i)

	list_of_date_matches = []
	for i,date in enumerate(list_of_dates):
		if date == closest_datetime:
			list_of_date_matches.append(i)
	#returns interested file (should just be one)
	return list_of_files[list(set(list_of_channel_matches) & set(list_of_date_matches))[0]]


##################################################################
# Above are functions for satellite data.  Below are functions for sensor
# and PV Output data
##################################################################

# This works for both sensor and pvoutput data:

def find_file_from_date(desired_date, filefolder, filetype = 'csv'):
    '''Input: datetime, folder, filetype; Output: file
    Usage: filefolder = "data/pvoutput/pvoutput6months/"
	desired_date = datetime(2014, 5, 5) #year, month, day [, hour, minute, second]
	find_file_from_date(desired_date, filefolder)'''
    data_files = os.listdir(filefolder)

    list_of_files = [] #contains all the files
    list_of_files_details = [] #contains information collected from filename
    for myfile in data_files:
        if (myfile[-2:] == filetype or myfile[-3:] == filetype): #only get netCDF by default
            list_of_files.append(myfile)
            list_of_files_details.append(myfile.split('.'))

    for i,val in enumerate(list_of_files_details):
        try:   
            if datetime.strptime(list_of_files_details[i][0], '%Y%m%d') == desired_date:
                return list_of_files[i]
        except:
            pass

def pad(x):
    time = x.astype(str).zfill(4)
    return time[:2] + ':' + time[2:]

def return_sensor_data(filename, filefolder):
    '''Input: desired file and folder
    Output: sensor data pandas dataframe
    Usage: filefolder = 'data/sensor_data/colorado6months/'
    filename = '20140401.csv'
    return_sensor_data(myfile, filefolder)'''
    
    df_header = pd.read_csv(filefolder + 'header.csv')
    headers = df_header.columns
    df_sensor = pd.read_csv(filefolder + filename,header=None) #sensors
    df_sensor.columns = headers
    df_sensor['MST'] = df_sensor['MST'].map(pad)
    #make a datetime index:
    df_sensor['datetime'] = pd.to_datetime(df_sensor['Year'].astype(str)+
                                           df_sensor['DOY'].astype(str)+
                                           df_sensor['MST'].astype(str), 
                                           format='%Y%j%H:%M')
    #convert to UTC time, website shows that they disregard daylight savings time
    df_sensor['datetime'] = df_sensor['datetime'] + pd.Timedelta(hours=7) 
    df_sensor.set_index(['datetime'],inplace=True) #set created column as index ...
    df_sensor = df_sensor.resample('H')# ... so that we can resample it (hourly)
    return df_sensor

def return_pvoutput_data(filename, filefolder):
    '''Input: Desired file and folder
    Output: PV Output dataframe
    Usage: filefolder = 'data/pvoutput/pvoutput6months/'
    filename = '20140401.csv'
    return_pvoutput_data(filename, filefolder)'''
    df_output = pd.read_csv(filefolder + filename) #pvoutput
    #df_output['datetime'] = df_output['datetime'] + pd.Timedelta(hours=6) #convert to utc time
    df_output['datetime'] = df_output['datetime'].apply(pd.to_datetime)
    df_output['datetime'] = df_output['datetime'] + pd.Timedelta(hours=6) #convert to utc time
    df_output.set_index(['datetime'],inplace=True) #set created column as index ...
    df_output = df_output.resample('H') # ...so that we can resample it (hourly)
    return df_output[['Power']]



