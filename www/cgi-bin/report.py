

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# enable debugging
import cgitb
cgitb.enable()
import cgi
from datetime import date, datetime, timedelta
import csv
import os
import geopy
from geopy.geocoders import Nominatim
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import geocoder

#html in python
print ('''Content-Type: text/html\n''')
print ('''
<html><head>
  <title>J^2</title>
  <meta name="description" content="fish fishing map with Doppler Radar Map" />
  <meta http-equiv="content-type" content="text/html" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<style>
body {background: #1339de;}
div#style {display : flex}
div#container
{        background: black;
 width: 50%;
  margin: 100px auto;
        color: white;
        border-radius: 1em;
        width: 1400px;
    height: 1125px;
    overflow:hidden;     /* if you don't want a scrollbar, set to hidden */
    overflow-x:hidden;   /* hides horizontal scrollbar on newer browsers */
    /* resize and min-height are optional, allows user to resize viewable area */
    -webkit-resize:vertical;
    -moz-resize:vertical;
    resize:vertical;
 //   min-height:1600px;
}
div#containerlil
{        background: black;
 width: 50%;
  margin: 100px auto;
        color: white;
        border-radius: 1em;
        width: 320px;
    height: 240px;
    overflow:hidden;     /* if you don't want a scrollbar, set to hidden */
    overflow-x:hidden;   /* hides horizontal scrollbar on newer browsers */
    /* resize and min-height are optional, allows user to resize viewable area */
    -webkit-resize:vertical;
    -moz-resize:vertical;
    resize:vertical;
 //   min-height:640px;
}
iframe#embedlil {
    width:320px; /* set this to approximate width of entire page you're embedding */
    height:240px; /* determines where the bottom of the page cuts off */
    margin-left:0px; /* clipping left side of page */
    margin-top:0px; /* clipping top of page */
    overflow:hidden;
    /* resize seems to inherit in at least Firefox */
    -webkit-resize:none;
    -moz-resize:none;
    resize:none;
}
</style>
<body><h1>FISHMAP.LFTR.biz</h1><h1>Doppler Map with Fishing Report!!!</h1></body> 
<script type="text/javascript" >
        function go() {
            var m3=document.getElementsByName("c");
            var m4=document.getElementsByName("d");
            window.location.href = "https://lftr.biz/cgi-bin/maplibre.py" + m3(0).value+"+"+ m4(0).value;
        }
       </script>
<script type="text/javascript" >
        function go2() {
            var m3=document.getElementsByName("e");
            var m4=document.getElementsByName("f");
            window.location.href = "https://lftr.biz/cgi-bin/maplibre.py" + m3(0).value+"+"+ m4(0).value;
        }
       </script>

<script type="text/javascript" >
        function go3() {
            var m5=document.getElementsByName("g");
            var m6=document.getElementsByName("h");
            window.location.href = "https://lftr.biz/cgi-bin/maplibre.py" + m5(0).value+"+"+ m6(0).value;
        }
       </script>
<script type="text/javascript" >
        function go4() {
            var m7=document.getElementsByName("i");
            var m8=document.getElementsByName("j");
            window.location.href = "https://lftr.biz/cgi-bin/maplibre.py" + m7(0).value+"+"+ m8(0).value;
        }
       </script>

</html>''')

print ('''<div id="style">
<form action="https://lftr.biz/cgi-bin/maplibre.py" onsubmit="go3();">
COORDINATES TO ADDRESS (LAT,LNG): <input type="text" name="g"><br>
ADDRESS TO COORDINATES (1234 STREET AVE, CITY, STATE): <input type="text" name="h"><br>
<input type="submit" value="Go Figure">
</form>
''')
print ('''
<h4>Alert to a new fishing location...!!!!</h4>
<form action="https://lftr.biz/cgi-bin/maplibre.py" onsubmit="go();">
Latitude (xxx.xxxx/-xxx.xxxx): <input type="text" name="c" value= "33.3866412"><br>
Longitude (xxx.xxxx/-xxx.xxxx): <input type="text" name="d" value= "-118.4734779"><br>
<input type="submit" value="Submit">
</form>
''')

### WEATHER ###
print ('''<h1>WEATHER BY LOCATION INPUT!!!</h1>''')
print ('''
<form action="https://lftr.biz/cgi-bin/maplibre.py" onsubmit="go4();">
Latitude (xxx.xxxx/-xxx.xxxx): <input type="text" name="i" value= "33.3866412"><br>
Longitude (xxx.xxxx/-xxx.xxxx): <input type="text" name="j" value= "-118.4734779"><br>
<input type="submit" value="Go Figure">
</form></div>
''')


#lat,lng,report tuple as list (commented out bc i am using a local csv file so as to WRITE reports to current locations)
#latlng = [(33.5987, -117.8826, ), (36.4147885,-118.9277509, ), (36.0765497,-118.9106086, ), (37.0396,-119.6483, ), (33.5901046, -117.870014, ), (33.5985056, -117.9033164, ), (33.6074678, -117.9309998, ), (33.6531, -118.0061, ), (33.7419998, -118.1875496, ), (34.4986553, -118.6108158, ), (34.2906126, -117.3599411, ), (34.565518, -114.3949421, ), (34.5133492, -114.3702769, ), (34.4548, -114.3755, ), (34.4495, -114.3724, ), (34.4494, -114.3712, )]

# open and read lat,lng,report tuple as list in local .csv
file = open("/var/www/fishloclist.csv", "r")
csv_reader = csv.reader(file)
#make csv content a python3 list
loc = []
for row in csv_reader:
    loc.append(row)


#Reload information for subbmitting reports
#pulls the variable values from the improved url
#saves the report to the list
#try or else just load with out updating via url when the url is standard

form = cgi.FieldStorage() 
try:
    lat = float(form.getvalue("c")) 
    lng = float(form.getvalue("d")) 
    coord = (lat,lng,'')
    loc.append(coord)
    with open('/var/www/fishloclist.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(loc)
        print ('location submited'+str(loc[-1]))

except:
    print ('')
try:
    report = str(form.getvalue("e")) 
    locnum = int(form.getvalue("f")) 
    loc[locnum].append(report)
    with open('/var/www/fishloclist.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(loc)
        print ('report submited'+str(loc[locnum]))
except:
    print ('')

geolocator = Nominatim(user_agent="LFTR_FISHMAP")

try:
    addressfield = form.getvalue("h") 
    coordfromaddress = (geolocator.geocode(str(addressfield)))
    coordfromaddresslat = coordfromaddress.latitude
    coordfromaddresslng = coordfromaddress.longitude
    print (coordfromaddresslat)
    print (coordfromaddresslng)
except:
    print ('')
try:    
    coord = str(form.getvalue("g"))
    print (coord) 
    location = (geolocator.reverse(coord)).address
    print (location)
except:
    print ('')
try:

    file = form.getvalue('videofile')
#    decodedfile = base64.b64decode(decodedfile)
    locnum = int(form.getvalue("f")) 
    os.remove('/var/www/fishvid/output'+str(locnum)+'.mp4')

    with open('/var/www/fishvid/output'+str(locnum)+'.mp4', 'wb') as bfile:
        bfile.write(file)
        bfile.close()
    print ('The video was successfully saved')

except:
    print ('')
