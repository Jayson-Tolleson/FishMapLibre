
#!/usr/bin/env python3
import cgitb
cgitb.enable()
import cgi
import time
import csv
import requests
import json
import subprocess
import os
from datetime import date, datetime, timedelta
import geopy
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
from urllib.request import urlopen
import geocoder
from flask import Flask, Response, request, render_template, redirect, url_for

app = Flask(__name__, static_folder='fishvid')
app.url_map.strict_slashes = False
@app.route('/fishmap')
def fishmap():
    def output():
        yield """<html><head><title>MapLibreGL</title>
<script src="https://unpkg.com/deck.gl@latest/dist.min.js"></script>
<script src="https://unpkg.com/@deck.gl/geo-layers@8.9.7/dist.min.js"></script>
<script src="https://unpkg.com/@deck.gl/mapbox@8.9.7/dist.min.js"></script>
<script src="https://unpkg.com/@deck.gl/core@8.9.7/dist.min.js"></script>
<script type="module "src="https://unpkg.com/@deck.gl/core@8.9.7/src/viewports/globe-viewport.ts"></script>
<script src="https://unpkg.com/@deck.gl/layers@8.9.7/dist.min.js"></script>
<script src="https://unpkg.com/@deck.gl/mesh-layers@8.9.7/dist.min.js"></script>
<script src="https://unpkg.com/@deck.gl/extensions@8.9.7/dist.min.js"></script>
<script src="https://unpkg.com/maplibre-gl@2.4.0/dist/maplibre-gl.js"></script>
<script src="https://unpkg.com/luma.gl@7.3.2/dist/es5/index.js"></script>
<script src="https://unpkg.com/@luma.gl/constants@8.5.19/dist/es5/index.js"></script>
<script src="https://unpkg.com/@luma.gl/core@8.5.19/dist/es5/index.js"></script>
<script src="https://unpkg.com/@loaders.gl/core@3.3.2/dist/es5/index.js"></script>
<script src="https://unpkg.com/gl-matrix@3.4.3/cjs/index.js"></script>
<script src="https://unpkg.com/null@2.0.0/index.js"></script>
<script src="https://unpkg.com/ts-node@10.9.1/dist/index.js"></script>
<script src="https://unpkg.com/tsc@2.0.4/bin/tsc.js"></script>
<script src="https://unpkg.com/typescript@5.0.3/lib/typescript.js"></script>
<link href="https://unpkg.com/maplibre-gl@2.4.0/dist/maplibre-gl.css" rel="stylesheet" />
  <meta name="description" content="fish fishing map with Doppler Radar Map" />
  <meta http-equiv="content-type" content="text/html" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<style>
body {background: #1339de;}
form {background-color:#1339de}
h1,h2,h3 {background-color:#009698;}
p {font-size: 13px;color: #1339de;background-color: #ffffff;}
div#style {display : flex}
video { background-color: black }
marquee {color: orange;}
div#scroll {overflow-y:scroll;height:600px;}
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
    -webkit-resize:vertical;
    -moz-resize:vertical;
    resize:vertical;}
div#containerlil
{        background: #009698;
 width: 50%;
  margin: 100px auto;
        color: white;
        border-radius: 1em;
        width: 1600px;
    height: 440px;
    overflow:hidden;     /* if you don't want a scrollbar, set to hidden */
    overflow-x:hidden;   /* hides horizontal scrollbar on newer browsers */
    -webkit-resize:vertical;
    -moz-resize:vertical;
    resize:vertical;}
div#containerpopup
{        background: #009698;
 width: 50%;
  margin: 10px auto;
        color: white;
        border-radius: 1em;
        width: 690px;
    height: 440px;
    overflow:hidden;     /* if you don't want a scrollbar, set to hidden */
    overflow-x:hidden;   /* hides horizontal scrollbar on newer browsers */
    /* resize and min-height are optional, allows user to resize viewable area */
    -webkit-resize:vertical;
    -moz-resize:vertical;
    resize:vertical;}
iframe#popup {
    width:680px; /* set this to approximate width of entire page you're embedding */
    height:440px; /* determines where the bottom of the page cuts off */
    margin-left:0px; /* clipping left side of page */
    margin-top:0px; /* clipping top of page */
    -webkit-resize:none;
    -moz-resize:none;
    resize:none;}
video {float:left;}
#marker {
background-image: url('https://lftr.biz/lftr4.png');
background-size: cover;
width: 20px;
height: 20px;
border-radius: 50%;
cursor: pointer;
border: 5px solid #555;}
.maplibregl-popup, .maplibregl-popup-content {width: 720px; height: 600px;}
#menu {
background: #009698;
position: absolute;
z-index: 1;
top: 10px;
right: 10px;
border-radius: 3px;
width: 120px;
border: 1px solid rgba(0, 0, 0, 0.4);
font-family: 'Open Sans', sans-serif;}
#menu a {
font-size: 13px;
color: #1339de;
display: block;
margin: 0;
padding: 0;
padding: 10px;
text-decoration: none;
border-bottom: 1px solid rgba(0, 0, 0, 0.25);
text-align: center;}
#menu a:last-child {border: none;}
#menu a:hover {background-color: #f8f8f8;color: #404040;}
#menu a.active {background-color: #3887be;color: #ffffff;}
#menu a.active:hover {background: #3074a4;}
.vidtext {    position: absolute;   top: 5px;   z-index: 10;}
</style>
<body><h1>FISHMAP.LFTR.biz</h1><h1>Doppler Map with Fishing Report!!!</h1></body>
<body>
<script type="text/javascript" >
        function go2() {
            var m3=document.getElementsByName("e");
            var m4=document.getElementsByName("f");
            window.location.href = "https://lftr.biz/cgi-bin/report.py" + m3(0).value+"+"+ m4(0).value;
        }
</script>"""
# open and read lat,lng,report tuple as list in local .csv
        file = open("/var/www/fishloclist.csv", "r")
        csv_reader = csv.reader(file)
#make csv content a python3 list
        loc = []
        for row in csv_reader:
            loc.append(row)
        length = len(loc)

##python moon in 20 lines
        moon = subprocess.Popen('sudo pyphoon -n 20',stdout=subprocess.PIPE,shell=True)
        x = 0
        moo =[]
        while x < 20:
            line = moon.stdout.readline().decode('utf-8')
            moo.append(line)
            x=x+1
##html elements in python (the body)
#contaier for asci moon AND FISHCATCH VIDEO
        vidlist=os.listdir('/var/www/fishvid/')
        vidlistlen = (len(vidlist))
        yield """<div id="containerlil"><video width="777" height="420" src="/fishvid/FishCatching.mp4" autoplay muted controls loop="true" type="video/mp4"></video>"""
        yield """<video height='420' width='777' muted autoplay controls id="Player" src='/fishvid/"""+vidlist[0]+""" ' onclick="this.paused ? this.play() : this.pause();">Your browser does not support the video tag.</video>"""
        yield """<script>var nextsrc = ["""
        x=1
        for x in range (vidlistlen):
            yield """'fishvid/"""+vidlist[x]+""" ',"""
        yield """];var elm = 0; var Player = document.getElementById('Player');Player.onended = function(){ if(++elm < nextsrc.length){Player.src = nextsrc[elm]; Player.play();  } }</script>"""
        yield """<div class="vidtext" style="z-index:22222;">"""
        x = 0
        while x < 20:
            line = str(moo[x])
            yield """<marquee><a href=''><div>"""+line+"""</div></a></marquee>"""
            x=x+1
        yield """</div></div>"""
#container for map
        yield """<div id="container"><nav id="menu"></nav><div id="map" style="width: 100%; height: 100%;    opacity: 1;"></div></div>"""
##javascript in html in python
        yield """<script>
const where = {
  zoom: 5,
  pitch: 62,
  longitude: -117,
  latitude: 33,
  maxPitch: 85,
  bearing: 44,
  altitude: 1.5,
};

let map = new maplibregl.Map({
 ...where,
  container: "map",
  center: [where.longitude, where.latitude],
  dragRotate: true,
  style: {
    version: 8,
    sources: {
      NexRAD: {
        type: "raster",
        tiles: [        "https://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi/wms?bbox={bbox-epsg-3857}&format=image/png&service=WMS&version=1.1.1&request=GetMap&srs=EPSG:3857&width=256&height=256&layers=nexrad-n0r-900913&transparent=true"],
        tileSize: 256,
        maxzoom: 12      },
     GoogleTraffic: {
        type: "raster",
        tiles: [" https://mt0.google.com/vt/lyrs=y,traffic,transit&x={x}&y={y}&z={z}"],
        tileSize: 256,
        maxzoom: 22      },
     GoogleSatellite: {
        type: "raster",
        tiles: [" https://mt0.google.com/vt/lyrs=s,traffic,transit&x={x}&y={y}&z={z}"],
        tileSize: 256,
        maxzoom: 22      },
      terrainSource: {
        type: "raster-dem",
        tiles: [
          "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"],
        encoding: "terrarium",
        tileSize: 256,
        maxzoom: 12 }, },
     layers: [
{ id: 'GoogleSatellite', type: 'raster', source: 'GoogleSatellite' },
{ id: 'GoogleTraffic', type: 'raster', source: 'GoogleTraffic' }, 
{ id: 'NexRAD', type: 'raster', source: 'NexRAD' }, 
],
     terrain: { source: 'terrainSource', exaggeration: 4, elevationOffset: 0 },

  }
});
map.addControl(
new maplibregl.NavigationControl({
visualizePitch: true,
showZoom: true,
showCompass: true
}));"""

##Popup Generator
##based on information in a flat file fishloclist.csv
#iterate all of the locations into popups with information
        x=0
        now = datetime.now()
        nowizzlot = datetime.now()+timedelta(days=3)
        for x in range(length):
            report = str(loc[x][-1]).replace('"', '')
            latitude = str(loc[x][0])
            longitude = str(loc[x][1])
            url = f"{'https://api.weather.gov/points/'}{latitude}{','}{longitude}"
            headers = {"User-Agent": "(fishmap-weather, jayson.tolleson@gmail.com)"}
            response = requests.get(url, headers = headers)
            points = json.loads(response.content.decode('utf-8'))
            office = points["properties"]["gridId"]
            gridX = points["properties"]["gridX"]  
            gridY = points["properties"]["gridY"]
            url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast"
            response = requests.get(url, headers = headers)
            weather = str(json.loads(response.content.decode('utf-8')))
            weathershort = weather[602:1750].replace('"', '')
            fullreport = str(loc[x]).replace('"', '')
            yield """var loc"""+str(x)+""" = ["""+(longitude)+""" , """+(latitude)+"""];"""
            yield """var el"""+str(x)+""" = document.createElement('div');el"""+str(x)+""".id = 'marker';"""
            yield """var popup"""+str(x)+""" = new maplibregl.Popup({ offset: 25 }).setHTML("<div id='scroll'><h1>Location: ( """ +latitude+ """ , """ +longitude+ """ ) </h1><p> Report: """ +report+ """ </p><p>Current Weather: """ +weathershort+ """ </p><div id='containerpopup'><iframe id='popup' src='https://lftr.biz/cgi-bin/roboweather.py?a="""+latitude+"""&b="""+longitude+""" '></iframe></div><h2>Location Video</h2><video width='320' height='240' controls autoplay src='/fishvid/temp"""+str(x)+""".mp4' type='video/mp4'></video><h1>Submit A New Fishing Report</h1><form action='https://lftr.biz/cgi-bin/report.py' onsubmit='go2();'>Enter Report: <input type='text' name='e' value= 'date, observation, tips & tricks'><br><input name ='f' value= """+str(x)+"""  type='hidden'><input type='submit' value='Submit'> </form><form enctype = 'multipart/form-data' action = 'https://lftr.biz:8084/uploader' method = 'post'><p>Upload File For The Location, ie. whats up on vid....(works on site, not app): <input type = 'file' name = 'file' /><input name ='f' value= """+str(x)+"""  type='hidden'></p><p><input type = 'submit' value = 'Upload' /></p><h3>FULL Report: </h3><h3> """+fullreport+weather+""" </h3></div>");"""
            yield """new maplibregl.Marker(el"""+str(x)+""" ).setLngLat(loc"""+str(x)+""" ).setPopup(popup"""+str(x)+""" ).addTo(map);"""
##continue JavaScript
#for map states, layers and layer buttons
        yield """map.on('idle', () => {
if (!map.getLayer('NexRAD') || !map.getLayer('GoogleTraffic') || !map.getLayer('GoogleSatellite')) {
return;}
const toggleableLayerIds = ['NexRAD', 'GoogleTraffic', 'GoogleSatellite'];
for (const id of toggleableLayerIds) {
if (document.getElementById(id)) {
continue;}
const link = document.createElement('a');
link.id = id;
link.href = '#';
link.textContent = id;
link.className = 'active';
link.onclick = function (e) {
const clickedLayer = this.textContent;
e.preventDefault();
e.stopPropagation();
const visibility = map.getLayoutProperty(
clickedLayer,
'visibility');
if (visibility === 'visible') {
map.setLayoutProperty(clickedLayer, 'visibility', 'none');
this.className = '';
} else {
this.className = 'active';
map.setLayoutProperty(
clickedLayer,
'visibility',
'visible');}};
const layers = document.getElementById('menu');
layers.appendChild(link);}});</script></body></html>"""
    return Response(output())
if __name__ == "__main__":  
    app.run(host='0.0.0.0', debug=True, ssl_context=('/var/security/lftr.biz.crt', '/var/security/lftr.biz.key'), port=8080)

