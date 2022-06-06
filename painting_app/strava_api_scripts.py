from social_django.models import UserSocialAuth
from django.db import transaction
import requests
import pandas as pd
import polyline
from .models import AllGridData, CanvasGridData
from .mapping import gridcoords_to_polygon, latlong_to_gridcoords
import datetime
import time
import numpy as np
# All things related to Strava API

class StravaApi:
    def __init__(self, user):
        strava_login = user.social_auth.get(provider='strava')
        self.access_token = strava_login.extra_data['access_token']

    # def get_user(self):
    #     x = 1

    def store_activities(self):
        x = 1
        activites_url = "https://www.strava.com/api/v3/athlete/activities"

        # Get activity data
        header = {'Authorization': 'Bearer ' + str(self.access_token)}
        activity_df_list = []
        for n in range(5):  # TODO: Change this to be higher
            param = {'per_page': 200, 'page': n + 1}

            activities_json = requests.get(activites_url, headers=header, params = param).json()
            if not activities_json:
                break
            activity_df_list.append(pd.json_normalize(activities_json))
        activities_df = pd.concat(activity_df_list)
        print('Importing', len(activities_df), 'activities')

        def clean_data(activities_df):
            def prep_activities_df(activities_df):
                activities_df['polylines'] = activities_df['map.summary_polyline']
                activities_df['activity_id'] = activities_df['id']
                activities_df['user_id'] = activities_df['athlete.id']
                activities_df['start_date_utc'] = activities_df['start_date']
                prepped_activities_df = activities_df[
                    ['user_id', 'activity_id', 'type', 'start_date_utc', 'start_date_local', 'timezone', 'polylines']]
                prepped_activities_df = prepped_activities_df.dropna(subset=['polylines'])
                prepped_activities_df['polylines'] = prepped_activities_df['polylines'].apply(polyline.decode)
                prepped_activities_df = prepped_activities_df.reset_index(drop=True)
                prepped_activities_df['start_date_utc'] = pd.to_datetime(prepped_activities_df['start_date_utc'])
                prepped_activities_df['start_date_local'] = pd.to_datetime(prepped_activities_df['start_date_local'])
                return prepped_activities_df
            #@transaction.atomic
            def prepped_to_sql(prepped_df):
                user_ids = []
                activities_ids = []
                lats = []
                longs = []
                times = []
                grid_lats = []
                grid_longs = []
                polys = []

                for ind, row in prepped_df.iterrows():
                    for lat, long in row['polylines']:
                        user_ids.append(row['user_id'])
                        activities_ids.append(row['activity_id'])
                        lats.append(lat)
                        longs.append(long)
                        times.append(row['start_date_utc'])
                        #         grid_lat, grid_long = latlong_to_gridcoords(lat,long)
                        grid_lats.append(None)
                        grid_longs.append(None)
                        polys.append(None)

                grid_df = pd.DataFrame(
                    {'userID': user_ids, 'activity_id': activities_ids, 'latitude': lats, 'longitude': longs,
                     'time': times, 'grid_lat': grid_lats, 'grid_long': grid_longs, 'polygon': polys})

                current_activities = list(AllGridData.objects.values_list('activity_id', flat=True).distinct())
                t0 = time.time()
                row_times = []
                n = 0
                for row in grid_df.itertuples():
                    if str(row.activity_id) not in current_activities:
                        t1 = time.time()
                        grid_lat, grid_long = latlong_to_gridcoords(row.latitude, row.longitude)
                        all_grid_instance = AllGridData(userID=row.userID, activity_id=row.activity_id,
                                                        latitude=row.latitude, longitude=row.longitude, time=row.time,
                                                        grid_lat = grid_lat, grid_long = grid_long)
                        t2 = time.time()
                        all_grid_instance.save()
                        t3 = time.time()
                        canvas_grid = CanvasGridData.objects.filter(grid_lat=all_grid_instance.grid_lat).filter(
                            grid_long=all_grid_instance.grid_long)
                        t4 = time.time()
                        if canvas_grid.exists():
                            t5 = time.time()
                            if row.time.replace(
                                    tzinfo=datetime.timezone.utc) > canvas_grid.values()[0]['time']:# datetime.datetime.strptime(row.time, '%Y-%m-%dT%H:%M:%SZ')
                                canvas_grid[0].delete()
                                canvas_instance = CanvasGridData(userID=row.userID, activity_id=row.activity_id,
                                                                 latitude=row.latitude, longitude=row.longitude,
                                                                 time=row.time, grid_lat = grid_lat,
                                                                 grid_long = grid_long)
                                canvas_instance.save()
                        else:
                            t6 = time.time()
                            canvas_instance = CanvasGridData(userID=row.userID, activity_id=row.activity_id,
                                                             latitude=row.latitude, longitude=row.longitude,
                                                             time=row.time, grid_lat = grid_lat,
                                                             grid_long = grid_long)
                            canvas_instance.save()
                        t7 = time.time()
                        row_times.append(t7-t1)
                        n+=1
                        if n %100 == 0:
                            print("row_time", np.mean(row_times), np.median(row_times))
                            print("allgrid_instance_time", t2 - t1)
                            print("allgrid_save_time", t3-t2)
                            print("filter_out_canvas_grid", t4-t3)
                            print("canvas_grid time ", t7-t4)

            prepped_df = prep_activities_df(activities_df)
            prepped_to_sql(prepped_df)

        clean_data(activities_df)
        return 'abc'
