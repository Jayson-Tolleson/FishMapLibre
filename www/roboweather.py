#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# enable debugging
import sys
import math
import time
import numpy as np
import datetime as dt
from datetime import date, datetime, timedelta
from geopy.geocoders import Nominatim
import requests
import json
import siphon
from siphon import catalog, ncss
from siphon.catalog import TDSCatalog
import bs4 as bs
import urllib.request
from netCDF4 import Dataset
import csv
from flask import Flask, Response, request, render_template, redirect, url_for

#time variables
day3 = dt.date.today()-dt.timedelta(days=3)
day7 = dt.date.today()-dt.timedelta(days=7)
tend=time.strftime("%Y"+"-"+"%m"+"-"+"%d"+"T"+"%H"+":"+"%M"+":"+"%S")
tend3 = str(day3)
tend7= str(day7)
now = datetime.now()
nowizzlot = datetime.now()+timedelta(days=5)
tminus7 = datetime.now()-timedelta(days=7)
date=time.strftime('%m'+' '+'%d,'+' '+'%Y'+' '+'%H'+':'+'%M'+':'+'%S'+' GMT')


app = Flask(__name__, static_folder='fishvid')
app.url_map.strict_slashes = False
@app.route('/roboweather/<lat>/<lng>')
def fishmap(lat,lng):
    def output():





#############################################################
####GFS 5Day Forecast
        url = 'http://thredds.ucar.edu/thredds/catalog/grib/NCEP/GFS/Global_0p25deg/catalog.xml?dataset=grib/NCEP/GFS/Global_0p25deg/Best'
        tds = catalog.TDSCatalog(url)
        datasets = list(tds.datasets)
        endpts = list(tds.datasets.values())
        nc = ncss.NCSS(endpts[0].access_urls['NetcdfSubset'])
        query = nc.query()
        query.lonlat_point(lng, lat).time_range(now, nowizzlot)
        query.variables('Temperature_surface', 'Wind_speed_gust_surface', 'Precipitation_rate_surface')
        data = nc.get_data(query)
        a = []
        b = []
        c = []
        e = []
        for d in data['time']:
 #   time = (d.isoformat())
            time = (d)
            a.append((time))
        for d in data['Temperature_surface']:
            t = (d-273.15)*(9/5)+32
            b.append((t))
        for d in data['Wind_speed_gust_surface']:
            w = (d*2.236694)
            c.append((w))
        for d in data['Precipitation_rate_surface']:
            r = ((d*10)/2.54)/60
            e.append((r))
        forecast = ['Date: '+str(m)+'    Temp(F): '+str(n)+'    Wind(mph): '+str(o)+'    Rain(in/hr): '+str(p) for m,n,o,p in zip(a,b,c,e)]
#############################################################################
##########HRRR FORECAST
        url = 'https://thredds.ucar.edu/thredds/catalog/grib/NCEP/HRRR/CONUS_2p5km/catalog.html?dataset=grib/NCEP/HRRR/CONUS_2p5km/Best'
        tds = catalog.TDSCatalog(url)
        datasets = list(tds.datasets)
        endpts = list(tds.datasets.values())
        query1 = ncss.NCSS(endpts[0].access_urls['NetcdfSubset']).query().lonlat_point(str(lng), str(lat)).time_range(now, nowizzlot).variables('Temperature_height_above_ground')
        query2 = ncss.NCSS(endpts[0].access_urls['NetcdfSubset']).query().lonlat_point(str(lng), str(lat)).time_range(now, nowizzlot).variables('Snow_depth_surface')
        query3 = ncss.NCSS(endpts[0].access_urls['NetcdfSubset']).query().lonlat_point(str(lng), str(lat)).time_range(now, nowizzlot).variables('Lightning_entire_atmosphere')
        query4 = ncss.NCSS(endpts[0].access_urls['NetcdfSubset']).query().lonlat_point(str(lng), str(lat)).time_range(now, nowizzlot).variables('Wind_speed_gust_surface')
        data1 = ncss.NCSS(endpts[0].access_urls['NetcdfSubset']).get_data(query1)
        data2 = ncss.NCSS(endpts[0].access_urls['NetcdfSubset']).get_data(query2)
        data3 = ncss.NCSS(endpts[0].access_urls['NetcdfSubset']).get_data(query3)
        data4 = ncss.NCSS(endpts[0].access_urls['NetcdfSubset']).get_data(query4)

        f = []
        g = []
        h = []
        i = []
        k = []
        for d in data1['time']:
            f.append(str(d))
        for d in data1['Temperature_height_above_ground']:
            g.append(str((d-273.15)*(9/5)+32))
        for d in data2['Snow_depth_surface']:
            h.append(str(d*39.3701))
        for d in data3['Lightning_entire_atmosphere']:
            i.append(str(d))
        for d in data4['Wind_speed_gust_surface']:
            k.append(str(d))
        forecast2 = ['Time: '+str(m)+'    Temp(F): '+str(n)+'    Snow Depth(inches): '+str(o)+'    Lightening: '+str(p)+'    Wind Speed Gust: '+str(q)+ '' for m,n,o,p,q in zip(f,g,b,c,e)]
#############################################################################
#############################################################################
#waves
##newport beach 17th st
        CSV_URL='https://thredds.ucar.edu/thredds/ncss/grid/grib/NCEP/WW3/Global/TwoD?var=Significant_height_of_combined_wind_waves_and_swell_surface&var=Direction_of_wind_waves_surface&var=Significant_height_of_wind_waves_surface&var=Primary_wave_direction_surface&var=Primary_wave_mean_period_surface&latitude=33.605711&longitude=-117.929239&time_start='+str(now)+'&time_end='+str(nowizzlot)+'&&&accept=csv'
        waves =[]
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            for row in my_list[1:8]:
                row = str('Date: '+row[0]+'lat,lng-Newport Point:  '+row[1]+'     Station: '+row[2]+','+row[3]+'     Direction(Deg),Height(Feet): '+row[7]+','+str((float(row[4]))*3.28084))
                waves.append(row)
#waves
##huntington City North Pier
        CSV_URL='https://thredds.ucar.edu/thredds/ncss/grid/grib/NCEP/WW3/Global/TwoD?var=Significant_height_of_combined_wind_waves_and_swell_surface&var=Direction_of_wind_waves_surface&var=Significant_height_of_wind_waves_surface&var=Primary_wave_direction_surface&var=Primary_wave_mean_period_surface&latitude=33.605711&longitude=-117.929239&time_start='+str(now)+'&time_end='+str(nowizzlot)+'&&&accept=csv'
        waves2 =[]
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list2 = list(cr)
            for row in my_list2[1:8]:
                row = str('Date: '+row[0]+'lat,lng-Huntington Beach, Ca northside pier : '+row[1]+'     Station: '+row[2]+','+row[3]+'      Direction(Deg),Height(Feet): '+row[7]+','+str((float(row[4]))*3.28084))
                waves2.append(row)
#waves
##loc
        CSV_URL='https://thredds.ucar.edu/thredds/ncss/grid/grib/NCEP/WW3/Global/TwoD?var=Significant_height_of_combined_wind_waves_and_swell_surface&var=Direction_of_wind_waves_surface&var=Significant_height_of_wind_waves_surface&var=Primary_wave_direction_surface&var=Primary_wave_mean_period_surface&latitude='+str(lat)+'&longitude='+str(lng)+'&time_start='+str(now)+'&time_end='+str(nowizzlot)+'&&&accept=csv'
        wavesloc =[]
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list3 = list(cr)
            for row in my_list3[1:8]:
                row = str('Date: '+row[0]+'lat,lng-this location by the sea: '+row[1]+'     Station: '+row[2]+','+row[3]+'     Direction(Deg),Height(Feet): '+row[7]+','+str((float(row[4]))*3.28084))
                wavesloc.append(row)
#############################################################################
        CSV_URL='https://www.ncei.noaa.gov/thredds/ncss/ncFC/fc-oisst-daily-avhrr-only-dly-prelim/OISST_Preliminary_Daily_AVHRR-only_Feature_Collection_best.ncd?var=sst&latitude='+str(lat)+'&longitude='+str(lng)+'&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start='+str(tminus7)+'&time_end='+str(now)+'&timeStride=1&&&accept=csv'
        sst=[]
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list4 = list(cr)
            for row in my_list4[1:8]:
                row = str('Date: '+row[0]+'lat,lng-this location by the sea: '+row[1]+','+row[2]+'     SST: '+str(((float(row[4]))*1.8)+32))
                sst.append(row)
#############################################################################





        yield """<html><head>
  <title>J^2</title>
  <meta name="description" content="RoboVoice Weather Forcast with Doppler Radar Map" />
  <meta http-equiv="content-type" content="text/html" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<style>
body {background: #1339de;}
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
iframe#embed
{
    width:1400px;       /* set this to approximate width of entire page you're embedding */
    height:1200px;      /* determines where the bottom of the page cuts off */
    margin-left:0px; /* clipping left side of page */
    margin-top:0px;  /* clipping top of page */
    overflow:hidden;
    /* resize seems to inherit in at least Firefox */
    -webkit-resize:none;
    -moz-resize:none;
    resize:none;
}
div#container2
{        background: black;
 width: 50%;
  margin: 100px auto;
        color: white;
        border-radius: 1em;
        width: 1400px;
    height: 1250px;
    overflow:hidden;     /* if you don't want a scrollbar, set to hidden */
    overflow-x:hidden;   /* hides horizontal scrollbar on newer browsers */
    /* resize and min-height are optional, allows user to resize viewable area */
    -webkit-resize:vertical;
    -moz-resize:vertical;
    resize:vertical;
 //   min-height:1600px;
}
iframe#embed2
{
    width:700px;       /* set this to approximate width of entire page you're embedding */
    height:600px;      /* determines where the bottom of the page cuts off */
    margin-left:0px; /* clipping left side of page */
    margin-top:0px;  /* clipping top of page */
    overflow:hidden;
    /* resize seems to inherit in at least Firefox */
    -webkit-resize:none;
    -moz-resize:none;
    resize:none;
}
</style>
<body>    <h1>Extended WEATHER</h1></body></html><h2></h2><h1>Coordinate Location JAYTVISION:</h1><h4></h4><section><div id="container2">
<div><h2>    SST  :  </h2></div>
<marquee>"""+str(sst)
        yield """</marquee>
<h4></h4>
<div><h2>    5 day JayT GFS Forecast:</h2></div>
<marquee>"""+str(forecast)
        yield """</marquee>
<h4></h4>
<div><h2>    8 HOUR JayT HRRR and GFS combo Forecast: </h2></div>
<marquee>"""+str(forecast2)+"""</marquee>
<h4></h4>
<div><h2>    5 day Wave Forecast(SURFING):</h2></div>
<marquee>"""+str(waves)
        yield """</marquee>
<marquee>"""+str(waves2)
        yield """</marquee>
<marquee>"""+str(wavesloc)
        yield """</marquee>
<h4></h4>
</div></section>"""
    return Response(output())
if __name__ == "__main__":  
    app.run(host='0.0.0.0', debug=True, ssl_context=('/var/security/lftr.biz.crt', '/var/security/lftr.biz.key'), port=8086)
