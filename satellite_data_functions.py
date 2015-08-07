import netCDF4
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap  #map stuff
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


def plot_satellite_image(filename):
	'''takes in a file and outputs a plot of satellite'''
	rootgrp = Dataset(filename, "a", format="NETCDF4")

	# print "type of data: ", rootgrp.data_model #netcdf3_classic, not netcdf4
	# myvars = []
	# for var in rootgrp.variables: #list of variables
	#     myvars.append(var)
	# print "variables in data: ", myvars
	# print "latitude of one point; ", rootgrp.variables['lat'][0][0] #verify that one latitude is where we expect

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

def return_satellite_data(filename):
	''' Input:  datetime, channel
		Output: lons, lats, data'''
	rootgrp = Dataset(filename, "a", format="NETCDF4") #generic name for data
	lons = rootgrp.variables['lon'][:] #extract lons ...
	lats = rootgrp.variables['lat'][:] #...lats...
	data = rootgrp.variables['data'][:] #...and data from netCDF file
	rootgrp.close() #need to close before you can open again
	return (lons, lats, np.squeeze(data))

