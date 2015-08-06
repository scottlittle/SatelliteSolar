#script for web scraping pvoutput.org for solar energy usage data
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import mechanize
import cookielib
import os

PVOUTPUT_USERNAME = os.environ['PVOUTPUT_USERNAME']
PVOUTPUT_PASSWORD = os.environ['PVOUTPUT_PASSWORD']
PVOUTPUT_API = os.environ['PVOUTPUT_API']

#login
cj = cookielib.CookieJar() #saves the cookie?
br = mechanize.Browser() #instansiates a browser
br.set_handle_robots(False) #I am not a robot...
br.set_cookiejar(cj) #use cookie?
br.open("http://pvoutput.org/") #open login page
br.select_form(nr=0) #select login form
br.form['login'] = PVOUTPUT_USERNAME #login using saved env vars
br.form['password'] = PVOUTPUT_PASSWORD #login using saved env vars
br.submit() #press enter
#print br.response().read() #see if it worked

#getting the actual data from a site
url = "http://pvoutput.org/intraday.jsp?id=5446&sid=5473&dt="
list_of_df_htmls = []
start_time = datetime(2014, 4, 1)
for i in range(0,183): #iterate over 6 months :for i in range(0,183): 
	start_str = start_time.strftime('%Y%m%d')
	br.open(url+start_str) #open desired page
	html = br.response().read() #read desired page
	df_html = pd.read_html(html)[0]

	#cleaning the data
	df_html.columns = pd.MultiIndex.from_arrays(df_html[df_html.index==1].values)
	df_html.drop(df_html.index[[0,1]],inplace=True)
	df_html['Power'] = df_html['Power'].str.replace(',','')
	df_html['Power'] = df_html['Power'].map(lambda x: x.rstrip('W'))

	def make_a_no(x):                  
	    try:
	        return int(x)
	    except:
	        x = 0 
	        return x
	    
	df_html['Power'] = df_html['Power'].map(make_a_no)
	df_html['datetime'] = pd.to_datetime(df_html['Date'] + ' ' + df_html['Time'], unit='h')
	df_html.set_index(['datetime'],inplace=True)
	df_html.to_csv('data/pvoutput/pvoutput6months/' + start_str + '.csv')
	start_time += timedelta(days=1) #update for next day
	



