from shapely.geometry import Polygon
from shapely import wkt
import folium
import geopandas as gpd
import pandas as pd
from paint_the_world.settings import BASE_DIR, ENGINE_URL
from sqlalchemy import create_engine
import os
"""
These scripts will be to create the GIS objects as well as mapping them onto the map
"""

def add_polylines(m, polylines, color, opacity ):
    # Add polylines to map from a list of polylines
    feature_group = folium.FeatureGroup()
    for line in polylines:
        folium.PolyLine(locations=line, color=color, opacity=opacity).add_to(feature_group)
    feature_group.add_to(m)

def latlong_to_gridcoords(lat, long, width = 0.001):
    """
    Determines the grid point a latitude and longitude would fall in if each grid space had dimensions lat/width and long/width

    For 0.001 that means there will be 360000 longitudes and 180000 latitude grid points over the entirety of the globe
    """
    grid_lat = round((lat + 90) / width)
    grid_long = round((long + 180) / width)
    return grid_lat, grid_long


def gridcoords_to_polygon(grid_lat, grid_long, color, time, weight = 0.1, fill_opacity = 0.5, width=0.001):
    """
    Turns a grid point, as defined in latlong_to_gridcoords() into a square polygon with side length = width
    """
    lat_center = grid_lat * width - 90
    long_center = grid_long * width - 180
    lats = [lat_center - width / 2, lat_center - width / 2, lat_center + width / 2, lat_center + width / 2]
    longs = [long_center - width / 2, long_center + width / 2, long_center + width / 2, long_center - width / 2]
    polygon = folium.Polygon(list(zip(lats, longs)), color = color, weight = weight, fill = True, fill_color = color, fill_opacity = fill_opacity, popup = "<b> Time: </b>"+ str(time))
    return polygon


def add_polygons(m, grid_lats, grid_longs, colors, times, path, weight = 0.1, fill_opacity = 0.5):
    # Add a list of polygons and colors to a given map
    # feature_group = folium.FeatureGroup()
    print('plotting', len(grid_lats), 'polygons')
    for n, (grid_lat, grid_long) in enumerate(zip(grid_lats, grid_longs)):
        # folium.GeoJson(wkt.loads(polygon.wkt), style_function=style_function_clr).add_to(m) #TODO: Only adding last color, may need to turn this into a chloropleth map
        # shapely_poly = wkt.loads(polygon.wkt)
        poly = gridcoords_to_polygon(grid_lat, grid_long, color = colors[n], time = times[n].strftime('%c'))
        poly.add_to(m)

    with open(path, 'w') as f:
        f.write(m._repr_html_())
    return path

def get_poly_details(map_type, userID = None):
    engine = create_engine(ENGINE_URL)
    current_users_df = pd.read_sql('SELECT * FROM \"painting_app_users\"', engine)
    canvas_df = pd.read_sql('SELECT * FROM \"painting_app_canvasgriddata\"', engine)
    canvas_df_clrs = canvas_df.merge(current_users_df[['id','color']], left_on ='userID', right_on = 'id')
    if map_type == 'full':
        grid_lats = canvas_df_clrs['grid_lat'].tolist()
        grid_longs = canvas_df_clrs['grid_long'].tolist()
        colors = canvas_df_clrs['color'].tolist()
        times = canvas_df_clrs['time'].tolist()
        return grid_lats, grid_longs, colors, times
    elif map_type == 'Self Portrait':
        all_points_df = pd.read_sql('SELECT * FROM \"painting_app_allgriddata\"', engine)

        personal_canvas = all_points_df.loc[all_points_df['userID'] == int(userID)]
        personal_canvas = pd.DataFrame(personal_canvas.sort_values('time').groupby(['grid_lat', 'grid_long']).last()).reset_index()
        personal_canvas = personal_canvas[
            ['activity_id', 'userID', 'latitude', 'longitude', 'time', 'grid_lat', 'grid_long']]
        personal_canvas_clrs = personal_canvas.merge(current_users_df[['id', 'color']], left_on='userID', right_on='id')
        grid_lats = personal_canvas_clrs['grid_lat'].tolist()
        grid_longs = personal_canvas_clrs['grid_long'].tolist()
        colors = personal_canvas_clrs['color'].tolist()
        times = personal_canvas_clrs['time'].tolist()
        return grid_lats, grid_longs, colors, times
    elif map_type == 'You vs the World':
        vs_world_df = canvas_df_clrs.copy()
        vs_world_df.loc[vs_world_df['userID'] != int(userID), 'color'] = 'BLACK'
        grid_lats = vs_world_df['grid_lat'].tolist()
        grid_longs = vs_world_df['grid_long'].tolist()
        colors = vs_world_df['color'].tolist()
        times = vs_world_df['time'].tolist()
        return grid_lats, grid_longs, colors, times


if __name__=="__main__":
    longitude = -82.68345
    latitude = 41.48026
    grid_lat, grid_long = latlong_to_gridcoords(latitude, longitude)
    poly = gridcoords_to_polygon(grid_lat, grid_long)
    x = 1