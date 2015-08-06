from noaaclass import noaaclass
from datetime import datetime, timedelta
import os

# The interval is allways a day to avoid the nights.
interval = timedelta(days=1)
# The nexts days and hours are in UTC format.
start = datetime(2014, 4, 1)
end = datetime(2014, 9, 30)
#denver before sunrise (5am in denver, 11am in gmt)
start_time = timedelta(hours=11, minutes=0, seconds=0)
#denver past sunset (10pm in denver, 4am in gmt)
end_time = timedelta(hours=4, minutes=0, seconds=0)

username = os.environ['NOAA_USERNAME']
password = os.environ['NOAA_PASSWORD']

noaa = noaaclass.connect(username, password)
data_template = {
    'id': '+',
    'north': 41.,
    'south': 38.,
    'west': -106.,
    'east': -103.,
    'coverage': ['NH'],
    'schedule': ['R'],
    'satellite': ['G15'],
    'channel': range(1,7),
    'format': 'NetCDF',
    'start': None,
    'end': None
}

request_to_do = []
while start < end:
    request = data_template.copy()
    request["start"] = start + start_time
    start = start + interval
    request["end"] = start + end_time
    request_to_do.append(request)
request_to_do = noaa.request.gvar_img.set(request_to_do, async=True)

save_list = open("list_5.txt", "a")
url = "http://download.class.ngdc.noaa.gov/download/"
for req in request_to_do:
    linea = url + req["id"] + "/001\n"
    save_list.write(linea)
    print linea

save_list.close()