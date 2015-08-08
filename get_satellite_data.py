# the directory where this is run must have the list.txt file that
# generates the local http files (http_files) with the command:
#  "wget -i list.txt" at the command line. This command should be
# run before running this script

import pandas as pd
import os
import glob
import requests

mypath = "data/satellite/colorado/summer6months/"

http_files = filter(os.path.isfile, glob.glob(mypath + "*")) #local http files
http_files.sort(key=lambda x: os.path.getmtime(x)) #sorts by time
http_files = [os.path.basename(i) for i in http_files] #extract filename
my_list_file = http_files[0] #pop out the list used to generate files in this dir
http_files = http_files[1:] #keep what is not popped out

with open(mypath + my_list_file) as f: #find noaa http files
    begin_urls = f.read().splitlines() #beginning part of urls to make downloads

len_begin_urls = len(begin_urls) #used for displaying completion percentage
for i, begin_url in enumerate(begin_urls):

	print "------------- ", 100.0 * i/len_begin_urls, " percent done overall---------------"

	df = pd.read_html(mypath + http_files[i],header=0)[0] #read local http file into df

	filenames = []
	for j in range(len(df)): #generate filenames from dataframe for data
	    filenames.append(df.loc[j, 'Name'])

	for filename in filenames:
		req = requests.get(begin_url + '/' + filename)
		with open( mypath + 'data/' + filename , 'wb' ) as fout: #save data!
			fout.write(req.content)


