#Satellite Solar
Galvanize capstone project for predicting solar energy usage from sensors and satellite data

##Background and Motivation
From satellite imagery data from NOAA and real physical sensors from NREL, create virtual sensors for anyone in the United States to use - possibly for predicting the energy from a solar panel setup.

Virtual sensors also have potential applications in other fields such as Internet of Things (IoT) and GIS applications.

##Data
Using photometric spectroscopy data from Colorado and corroborating that with aerosol satellite images, we can create virtual sensors that inform us how much solar can be produced in a given geographical location in the United States.

##Method
By using machine learning algorithms (extra trees random forest regressor) on the data, we can reveal empirical trends in the data that let us reproduce the sensor data collected in Colorado.  Using this data in another location in the contenental United States, should allow one to predict the solar energy production.  This will be confirmed by using the virtual sensor information to inform silicon-based solar panel power production.

##Web Interface
The web interface allows for a user to adjust the date and time and see the amount of solar energy produced for the number of solar panels selected.  Future implementations would also include pricing information such as selecting solar panels from different solar cell companies and comparing the cost and energy savings.
