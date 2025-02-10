# Important import

import numpy as np
import pandas as pd
import streamlit as st

import os
import time
from datetime import *

import folium
from collections import defaultdict, OrderedDict
from folium.plugins import HeatMapWithTime
from folium.plugins import HeatMap

from streamlit_folium import st_folium, folium_static

import matplotlib.pyplot as plt
import matplotlib as mpl
import branca


# Functions to transform the data

def get_latitude(dt):
    return float(dt.split(',')[1])
def get_longitude(dt):
    return float(dt.split(',')[0])
def get_dom(dt):
    return dt.day
def get_weekday(dt):
    return dt.weekday() + 1
def get_hour(dt):
    return dt.hour
def get_month(dt):
    return dt.month
def get_date(dt):
    return dt.date()
def get_week(dt):
    return dt.date().isocalendar()[1]
def get_hour_count(dtf):
    hour = dtf.hour
    weekday = dtf.weekday()
    time = datetime.strptime("03/02/21 16:30", "%d/%m/%y %H:%M")
    min_ = time.minute
    if weekday == 5:
        return 60*24*(weekday-5) + hour + min_
    elif weekday == 6:
        return 60*24*(weekday-5) + hour + min_
    elif weekday == 0:
        return 60*24*(weekday+2) + hour + min_
    elif weekday == 1:
        return 60*24*(weekday+2) + hour + min_
    elif weekday == 2:
        return 60*24*(weekday+2) + hour + min_
    elif weekday == 3:
        return 60*24*(weekday+2) + hour + min_
    elif weekday == 4:
        return 60*24*(weekday+2) + hour + min_
    
    
# We will collect all available files and transform the data

def load_model():
    all_files = os.listdir("release/taxi_log_2008_by_id/")  
    location_history = pd.read_fwf("release/taxi_log_2008_by_id/1.txt", delimiter = ',', names = ["id", "date/time", "lat/lon"])
    y = 0
    for i in all_files[1:25]:
        print(y)
        y += 1
        file_path = "release/taxi_log_2008_by_id/" + i
        df = pd.read_fwf(file_path, delimiter = ',', names = ["id", "date/time", "lat/lon"])
        location_history = location_history.append(df)
        
    location_history['date/time'] = location_history['date/time'].map(pd.to_datetime)

    location_history['latitude'] = location_history['lat/lon'].map(get_latitude)
    location_history['longitude'] = location_history['lat/lon'].map(get_longitude)
    location_history = location_history.drop(['lat/lon'], axis = 1)

    location_history['date'] = location_history['date/time'].map(get_date)
    location_history['week'] = location_history['date/time'].map(get_week)
    location_history['month'] = location_history['date/time'].map(get_month)
    location_history['day'] = location_history['date/time'].map(get_dom)
    location_history['weekday'] = location_history['date/time'].map(get_weekday)
    location_history['hour'] = location_history['date/time'].map(get_hour)

    location_history['day_hour_min_position'] = location_history['date/time'].map(get_hour_count)
    
    return location_history
        
    
# Load and transform the dataset

location_history  = load_model()
location_beijing=[39.93089, 116.36132]


# All the coordinates of our dataset on a map

def map0():
    st.header("Coordinates of our dataset on a map")
    map_osm = folium.Map(location=location_beijing, zoom_start=11)

    location_history.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]], 
                                                  radius=1)
                                                 .add_to(map_osm), axis=1)
    folium_static(map_osm)
    
    
# Heatmap by hours and weekday

def map1():
    st.header("Taxies in Beijing by Date/Time")
    with st.expander("HeatMap"):
        
        tab1, tab2, tab3 = st.tabs(["Hour (1)", "Hour (2)", "Weekday"])
    
    with tab1:
        data = defaultdict(list)
        for r in location_history.itertuples():
            data[r.hour].append([r.latitude, r.longitude])
            
        data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))

        m = folium.Map(location_beijing,
                    tiles='stamentoner',
                    zoom_start=11)

        hm = HeatMapWithTime(data=list(data.values()),
                            index=list(data.keys()), 
                            radius=10,
                            auto_play=True,
                            max_opacity=1)
        hm.add_to(m)
        
        folium.TileLayer('Stamen Terrain').add_to(m)
        folium.TileLayer('Stamen Toner').add_to(m)
        folium.TileLayer('Stamen Water Color').add_to(m)
        folium.TileLayer('cartodbpositron').add_to(m)
        folium.TileLayer('cartodbdark_matter').add_to(m)
        folium.LayerControl().add_to(m)
    
        folium_static(m)
    
    with tab2:
        df_hour_list = []
        for hour in location_history.hour.sort_values().unique():
            df_hour_list.append(location_history.loc[location_history.hour == hour, ['latitude', 'longitude', 'count']].groupby(['latitude', 'longitude']).sum().reset_index().values.tolist())
        base_heattimemap = folium.Map(location=[39.93089, 116.36132], zoom_start=11)
        HeatMapWithTime(df_hour_list, radius=8, gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'}, min_opacity=0.8, max_opacity=1, use_local_extrema=True).add_to(base_heattimemap)

        folium_static(base_heattimemap)
        
    with tab3:
        st.header("HeatMap by Weekday")
        data = defaultdict(list)
        for r in location_history.itertuples():
            data[r.weekday].append([r.latitude, r.longitude])
            
        data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))

        m = folium.Map(location_beijing,
                    tiles='stamentoner',
                    zoom_start=11)

        hm = HeatMapWithTime(data=list(data.values()),
                            index=list(data.keys()), 
                            radius=11,
                            auto_play=True,
                            max_opacity=1)
        hm.add_to(m)
        
        folium.TileLayer('Stamen Terrain').add_to(m)
        folium.TileLayer('Stamen Toner').add_to(m)
        folium.TileLayer('Stamen Water Color').add_to(m)
        folium.TileLayer('cartodbpositron').add_to(m)
        folium.TileLayer('cartodbdark_matter').add_to(m)
        folium.LayerControl().add_to(m)
        
        folium_static(m)

        
# HeatMap of the Taxis every 10 min

def map2():
    st.header("Taxis in Beijing every 10 min")
    data = defaultdict(list)
    for r in location_history.itertuples():
        data[r.day_hour_min_position].append([r.latitude, r.longitude])
        
    data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))

    m = folium.Map(location_beijing,
                   tiles='stamentoner',
                   zoom_start=11)

    hm = HeatMapWithTime(data=list(data.values()),
                         index=list(data.keys()), 
                         radius=10,
                         auto_play=False,
                         max_opacity=1,
                         speed_step =10 )
    hm.add_to(m)

    folium_static(m)

    
# Global Heatmap without Date/Time

def map3():
    st.header("Taxies in Beijing without Date/Time")
    location_history['count'] = 1 
    base_heatmap = folium.Map(location=[39.93089, 116.36132], zoom_start=10)
    HeatMap(data=location_history[['latitude', 'longitude', 'count']].groupby(['latitude', 'longitude']).sum().reset_index().values.tolist(), radius=14, max_zoom=4).add_to(base_heatmap)
    folium_static(base_heatmap)

    
# Creation of the grid

def get_geojson_grid(upper_right, lower_left, n=6):
    """Returns a grid of geojson rectangles, and computes the exposure in each section of the grid based on the vessel data.

    Parameters
    ----------
    upper_right: array_like
        The upper right hand corner of "grid of grids" (the default is the upper right hand [lat, lon] of the USA).

    lower_left: array_like
        The lower left hand corner of "grid of grids"  (the default is the lower left hand [lat, lon] of the USA).

    n: integer
        The number of rows/columns in the (n,n) grid.

    Returns
    -------

    list
        List of "geojson style" dictionary objects   
    """

    all_boxes = []

    lat_steps = np.linspace(lower_left[0], upper_right[0], n+1)
    lon_steps = np.linspace(lower_left[1], upper_right[1], n+1)

    lat_stride = lat_steps[1] - lat_steps[0]
    lon_stride = lon_steps[1] - lon_steps[0]

    for lat in lat_steps[:-1]:
        for lon in lon_steps[:-1]:
            # Define dimensions of box in grid
            upper_left = [lon, lat + lat_stride]
            upper_right = [lon + lon_stride, lat + lat_stride]
            lower_right = [lon + lon_stride, lat]
            lower_left = [lon, lat]

            # Define json coordinates for polygon
            coordinates = [
                upper_left,
                upper_right,
                lower_right,
                lower_left,
                upper_left
            ]

            geo_json = {"type": "FeatureCollection",
                        "properties":{
                            "lower_left": lower_left,
                            "upper_right": upper_right
                        },
                        "features":[]}

            grid_feature = {
                "type":"Feature",
                "geometry":{
                    "type":"Polygon",
                    "coordinates": [coordinates],
                }
            }

            geo_json["features"].append(grid_feature)

            all_boxes.append(geo_json)

    return all_boxes


# Map density

def map4():
    st.header("Density between 2 hours")
    values = st.slider(
        'Select a range of hours',
        0, 23, (8, 16))
    n = st.slider(
        'Select a number of grid',
        1, 50, (20))
    min_hour = values[0]
    max_hour = values[1]
    #boundaries of the main rectangle
    upper_right = [40.02301836689508, 116.52767681309274]
    lower_left = [39.827866917680026, 116.25867593822134]
    
    # Creating a grid of nxn from the given cordinate corners     
    grid = get_geojson_grid(upper_right, lower_left , n)
    # Holds number of points that fall in each cell & time window if provided
    counts_array = []
    
    # Adding the total number of coordinates to each cell
    for box in grid:
        # get the corners for each cell
        upper_right = box["properties"]["upper_right"]
        lower_left = box["properties"]["lower_left"]# check to make sure it's in the box and between the time window if time window is given 
        mask = ((location_history.latitude <= upper_right[1]) & (location_history.latitude >= lower_left[1]) &
            (location_history.longitude <= upper_right[0]) & (location_history.longitude >= lower_left[0]) &
            (location_history.hour >= min_hour) & (location_history.hour <= max_hour))# Number of points that fall in the cell and meet the condition 
        counts_array.append(len(location_history[mask]))# creating a base map 
    m = folium.Map(zoom_start = 10, location=location_beijing)# Add GeoJson to map
    for i, geo_json in enumerate(grid):
        relativeCount = counts_array[i]*100/sum(counts_array)
        color = plt.cm.YlGn(relativeCount)
        color = mpl.colors.to_hex(color)
        gj = folium.GeoJson(geo_json,
                style_function=lambda feature, color=color: {
                    'fillColor': color,
                    'color':"gray",
                    'weight': 0.5,
                    'dashArray': '6,6',
                    'fillOpacity': '0.8',
                })
        m.add_child(gj)
        
    colormap = branca.colormap.linear.YlGn_09.scale(0, 10)
    colormap = colormap.to_step(index=[0, 0.3, 0.6, 0.8 , 1])
    colormap.caption = 'Relative density of fleet activity per cell'
    colormap.add_to(m)
    folium_static(m)# limiting time window for our data to 8 am - 5 pm and also grid is 20 x 20 

    
# 3 trips of 3 taxies
def map5():
    st.header("3 trips of 3 taxies")
    m2=folium.Map(location=location_beijing,tiles='stamentoner',zoom_start=11)

    f1=folium.FeatureGroup("Vehicle 1")
    f2=folium.FeatureGroup("Vehicle 3")
    f3=folium.FeatureGroup("Vehicle 10")

    line_1=folium.vector_layers.PolyLine(location_history[location_history["id"] ==1][['latitude', 'longitude']],popup='<b>Path of Vehicle_1</b>',tooltip='Vehicle_1',color='blue',weight=1).add_to(f1)
    line_2=folium.vector_layers.PolyLine(location_history[location_history["id"] ==3][['latitude', 'longitude']],popup='<b>Path of Vehicle_3</b>',tooltip='Vehicle_3',color='red',weight=1).add_to(f2)
    line_3=folium.vector_layers.PolyLine(location_history[location_history["id"] ==10][['latitude', 'longitude']],popup='<b>Path of Vehicle_10</b>',tooltip='Vehicle_10',color='green',weight=1).add_to(f3)

    f1.add_to(m2)
    f2.add_to(m2)
    f3.add_to(m2)
    folium.LayerControl().add_to(m2)
    folium_static(m2)

    
# Trips of the taxi 10 per day

def map6():
    st.header("Trips of the taxi 10 per day")
    data = defaultdict(list)
    for r in location_history[location_history["id"] ==10].itertuples():
        data[r.weekday].append([r.latitude, r.longitude])
        
    data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))

    m = folium.Map(location_beijing,
                   tiles='stamentoner',
                   zoom_start=11)

    for i in data.keys():
        name_FeatureGroup = "day " + str(i) 
        name_tooltip = "day_" + str(i)
        f=folium.FeatureGroup(name_FeatureGroup)
        line=folium.vector_layers.PolyLine(data[i],popup='<b>Path of Vehicle_10</b>',tooltip=name_tooltip ,color='blue',weight=3).add_to(f)
        f.add_to(m)

    folium.LayerControl().add_to(m)

    folium_static(m)
    
    
def main():
    st.title("Analysis of our dataset")
    st.write("here is our transformed database:")
    st.write(location_history)
    map0()
    map3()
    map1()
    map2()
    map4()
    map5()
    map6()
