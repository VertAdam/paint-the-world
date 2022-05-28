from shapely.geometry import Polygon
import folium
import geopandas as gpd
import pandas as pd

"""
These scripts will be to create the GIS objects as well as mapping them onto the map
"""



def add_polylines(m, polylines, color, opacity=0.6):
    # Creates polylines from a list of polylines in prepped_df
    feature_group = folium.FeatureGroup()
    for line in polylines:
        folium.PolyLine(locations=line, color=color, opacity=opacity).add_to(feature_group)
    feature_group.add_to(m)


class painting:
    """
    This class will be used to create the GIS objects and final maps using the data from the database
    """
    def __init__(self,width):
        self.width = width
        self.polygon_data = pd.read_csv()
        self.user_data = pd.read_csv()
    def latlong_to_gridcoords(self, lat, long):
        """
        Determines the grid point a latitude and longitude would fall in if each grid space had dimensions lat/width and long/width

        For 0.001 that means there will be 360000 longitudes and 180000 latitude grid points over the entirety of the globe
        """
        grid_lat = round((lat + 90) / width)
        grid_long = round((long + 180) / width)
        return grid_lat, grid_long


def gridcoords_to_polygon(grid_lat, grid_long, width=0.001):
    """
    Turns a grid point, as defined in get_gridcoords() into a square polygon with side length = width
    """
    lat_center = grid_lat * width - 90
    long_center = grid_long * width - 180
    lats = [lat_center - width / 2, lat_center - width / 2, lat_center + width / 2, lat_center + width / 2]
    longs = [long_center - width / 2, long_center + width / 2, long_center + width / 2, long_center - width / 2]
    polygon = Polygon(zip(longs, lats))
    return polygon