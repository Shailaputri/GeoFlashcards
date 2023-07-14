import folium
import fiona
import pandas as pd
import geopandas as gpd
from folium.features import DivIcon
from folium import IFrame
import base64

def generate_map():

    zoom = 4.4

    state_geo = f'india_states_with_ladakh.geojson'

    gdf = gpd.read_file(state_geo)
    data_frame = pd.read_csv('biodiversity_heritage_sites_details.csv')

    name_list = data_frame['Name of the Site'].tolist()
    state_list = data_frame['State'].tolist()
    district_list = data_frame['Name of the District'].tolist()
    description_list = data_frame['Importance of the area'].tolist()

    lat_list = data_frame['Lat'].tolist()
    lon_list = data_frame['Lon'].tolist()

    fi = fiona.open(state_geo)

    top = fi.bounds[3]
    bottom = fi.bounds[1]
    left = fi.bounds[0]
    right = fi.bounds[2]

    m = folium.Map(
        location=[(top+bottom)/2,((left+right)/2)],
        zoom_start=zoom,
        minZoom=zoom-2,
        maxZoom=zoom+5,
        # resize=False,
        # zoomControl= False,
        # zoomAnimation= False,
        # trackResize= True, 
        # touchZoom=False,
        # boxZoom=False,
        # doubleClickZoom=False,
        scrollWheelZoom= 'center',
        # singleClickZoom=False,
        dragging=True,
        tiles='OpenStreetMap',
        # maxBoundsViscosity= 1.0,
        # interactive= False,
        # tap=False
        )

    choropleth = folium.Choropleth(
        geo_data=gdf,
        name='choropleth',
        fill_color='white',
        fill_opacity=0.8,
        line_opacity=0.8,
        highlight=False,
        line_color='black',
    ).add_to(m)

    for item in name_list:

        lat = lat_list[name_list.index(item)]
        lon = lon_list[name_list.index(item)]

        state = str(state_list[name_list.index(item)])
        district = str(district_list[name_list.index(item)])
        description = str(description_list[name_list.index(item)])

        state_html = '' if (state=='nan') else "<p style=\"font-size:12px\">State: "+state+"</p>"
        district_html = '' if (district=='nan') else "<p style=\"font-size:12px\">District:"+district+"</p>"
        description_html = '' if (description=='nan') else "<p style=\"font-size:12px\">"+description+"</p>"

        html="<div style=\"@import url('https://fonts.googleapis.com/css?family=Roboto+Condensed');font-family: 'Roboto Condensed', sans-serif;\">"+"<h5>"+item+"</h5>"+state_html+district_html+description_html

        # resolution, width, height = 10, 50, 25
        iframe = IFrame(html, width=250, height=200)
        popup = folium.Popup(iframe, max_width=1000)
        icon = folium.Icon(color="orange", icon="pagelines", prefix='fa')
        marker = folium.Marker(location=[lat, lon], popup=popup, tooltip=item, icon=icon)
        marker.add_to(m)

    m.save('../map_biodiversity_heritage_sites.html')

if __name__=='__main__':
    generate_map()
