from django.shortcuts import render, redirect
import folium
from .models import CanvasGridData
from .mapping import add_polygons, get_poly_details
import random
from .strava_api_scripts import StravaApi
from paint_the_world.settings import BASE_DIR, ENGINE_URL
import os
import pandas as pd
from sqlalchemy import create_engine

def not_connected_view(request):
    # map1 = folium.Map(tiles='stamentoner', location = [43.45005, -80.42766], zoom_start = 15,prefer_canvas = True)
    # grid_lats = list(CanvasGridData.objects.values_list('grid_lat',flat = True))
    # grid_longs = list(CanvasGridData.objects.values_list('grid_long',flat = True))
    # times = list(CanvasGridData.objects.values_list('time', flat=True))
    # clrs = ['red','red','red','red','blue','orange']
    #
    # map1 = add_polygons(map1, grid_lats,grid_longs , colors = random.choices(clrs, k = len(grid_lats)), times = times)
    # map1 = map1._repr_html_()
    #
    # context ={
    #     'map1':map1
    # }
    path = os.path.join(BASE_DIR,'templates','maps','full_map.txt')
    context ={
        'map_path': path
    }
    return render(request, 'painting_app/not_connected.html', context) # Pulls index map

def connected_view(request):
    # Get Users Keys
    user = request.user
    api_service = StravaApi(user)
    path = os.path.join(BASE_DIR, 'templates', 'maps', 'full_map.txt')
    api_service.get_user_data()

    # Load in User and Activity Data
    # api_service.store_user() TODO: Add this feature in
    new_activities = api_service.store_activities()

    response = redirect('/connected/FullPainting')
    return response



def connected_fullpainting(request):
    path = os.path.join(BASE_DIR, 'templates', 'maps', 'full_map.txt')
    context ={
        'map_path': path
    }
    return render(request, 'painting_app/connected.html', context)

def self_portrait(request):
    userID = request.user.social_auth.get(provider='strava').uid
    path = os.path.join(BASE_DIR, 'templates', 'maps', 'self_portrait_%s.txt' %userID)

    map1 = folium.Map(tiles='stamentoner', location = [43.45005, -80.42766], zoom_start = 15,prefer_canvas = True)

    grid_lats, grid_longs, colors, times = get_poly_details('Self Portrait', userID=userID)
    add_polygons(map1, grid_lats,grid_longs, path =  path, colors = colors, times = times)

    context ={
        'map_path': path
    }
    return render(request, 'painting_app/connected.html', context)


def vs_world(request):
    userID = request.user.social_auth.get(provider='strava').uid
    path = os.path.join(BASE_DIR, 'templates', 'maps', 'vs_world_%s.txt' % userID)

    map1 = folium.Map(tiles='stamentoner', location=[43.45005, -80.42766], zoom_start=15, prefer_canvas=True)

    grid_lats, grid_longs, colors, times = get_poly_details('You vs the World', userID=userID)
    add_polygons(map1, grid_lats, grid_longs, path=path, colors=colors, times=times)

    context = {
        'map_path': path
    }
    return render(request, 'painting_app/connected.html', context)

def change_color(request):
    engine = create_engine(ENGINE_URL)
    userID = request.user.social_auth.get(provider = 'strava').uid
    current_users_df = pd.read_sql('SELECT * FROM \"painting_app_users\"', engine)

    clr = request.GET.get('name')
    current_users_df.loc[current_users_df['id'] ==  int(userID), 'color'] = [clr]
    current_users_df.to_sql("painting_app_users", engine, if_exists='replace', index=False)

    response = redirect('/connected/SelfPortrait')
    return response