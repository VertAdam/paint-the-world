from django.shortcuts import render
import folium
from .models import CanvasGridData
from .mapping import add_polygons
import random
from .strava_api_scripts import StravaApi

def not_connected_view(request):
    map1 = folium.Map(tiles='stamentoner', location = [43.45005, -80.42766], zoom_start = 15,prefer_canvas = True)
    grid_lats = list(CanvasGridData.objects.values_list('grid_lat',flat = True))
    grid_longs = list(CanvasGridData.objects.values_list('grid_long',flat = True))
    clrs = ['red','red','red','red','blue','orange']

    map1 = add_polygons(map1, grid_lats,grid_longs , colors = random.choices(clrs, k = len(grid_lats)))
    map1 = map1._repr_html_()
    context ={
        'map1':map1
    }
    return render(request, 'painting_app/index.html', context) # Pulls index map

def connected_view(request):
    # Get Users Keys
    user = request.user
    api_service = StravaApi(user)

    # Load in User and Activity Data
    # api_service.store_user() TODO: Add this feature in
    api_service.store_activities()

    map1 = folium.Map(tiles='stamentoner', location = [43.45005, -80.42766], zoom_start = 15,prefer_canvas = True)
    map1 = map1._repr_html_()
    context ={
        'map1':map1
    }
    return render(request, 'painting_app/index.html', context) # Pulls index map
