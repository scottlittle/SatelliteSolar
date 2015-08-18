#Satellite Solar
Galvanize capstone project for predicting solar energy usage from sensors and satellite data

##Background and Motivation
From satellite imagery data from the National Oceanic and Atmospheric Administration (NOAA) and real physical sensors from the National Renewable Energy Lab (NREL), predict the power for a solar panel setup at a given date and time.

In the process of modelling solar power from satellite imagery, ground sensors are simulated in an intermediate step in what can be coined as "virtual sensors."  Virtual sensors have potential applications in other fields such as Internet of Things (IoT).

##Data
Using photometric spectroscopy data from Colorado and corroborating that with aerosol satellite images, we can create virtual sensors that inform us how much solar can be produced in a given geographical location in the United States.

##Method
By using machine learning algorithms (extra trees random forest regressor) on the data, we can reveal empirical trends in the data that let us reproduce the sensor data collected in Colorado and predict the solar panel power production.

##Web Interface
The web interface allows for a user to adjust the date and time and see the amount of solar energy produced for the number of solar panels selected.  Future implementations would also include pricing information such as selecting solar panels from different solar cell companies and comparing the cost and energy savings.

##Presentation
[Here's a snapshot of the presentation.](https://github.com/scottlittle/SatelliteSolar/blob/master/documentation/Satellite%20Solar%20-%20Galvanize%20Capstone.pdf)
