from shapely.geometry import Polygon
from shapely import wkt
import folium
import geopandas as gpd
import pandas as pd

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


def gridcoords_to_polygon(grid_lat, grid_long, color, weight = 0.1, fill_opacity = 0.5, width=0.001):
    """
    Turns a grid point, as defined in latlong_to_gridcoords() into a square polygon with side length = width
    """
    lat_center = grid_lat * width - 90
    long_center = grid_long * width - 180
    lats = [lat_center - width / 2, lat_center - width / 2, lat_center + width / 2, lat_center + width / 2]
    longs = [long_center - width / 2, long_center + width / 2, long_center + width / 2, long_center - width / 2]
    print(lats, longs)
    polygon = folium.Polygon(list(zip(lats, longs)), color = color, weight = weight, fill = True, fill_color = color, fill_opacity = fill_opacity)
    return polygon


def add_polygons(m, grid_lats, grid_longs, colors , weight = 0.1, fill_opacity = 0.5):
    # Add a list of polygons and colors to a given map
    # feature_group = folium.FeatureGroup()
    print('plotting', len(grid_lats), 'polygons')
    for n, (grid_lat, grid_long) in enumerate(zip(grid_lats, grid_longs)):
        # folium.GeoJson(wkt.loads(polygon.wkt), style_function=style_function_clr).add_to(m) #TODO: Only adding last color, may need to turn this into a chloropleth map
        # shapely_poly = wkt.loads(polygon.wkt)
        poly = gridcoords_to_polygon(grid_lat, grid_long, color = colors[n])
        poly.add_to(m)
        # a = folium.Polygon([(lat,long) for long,lat in list(polygon.exterior_ring.coords)], color = colors[n], weight = weight, fill = True, fill_color = colors[n], fill_opacity = fill_opacity).add_to(m)
        # a.save('a.html')
        # break

    m.save('a.html')
    # feature_group.add_to(m)
    return m


if __name__=="__main__":
    longitude = -82.68345
    latitude = 41.48026
    grid_lat, grid_long = latlong_to_gridcoords(latitude, longitude)
    poly = gridcoords_to_polygon(grid_lat, grid_long)
    x = 1