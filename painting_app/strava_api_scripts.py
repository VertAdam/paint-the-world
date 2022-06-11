from social_django.models import UserSocialAuth
import requests
import pandas as pd
import polyline
from sqlalchemy import create_engine
from paint_the_world import settings
import random
from painting_app.helpers import full_grid_to_tupled_df, tupled_df_to_full_grid

# All things related to Strava API

class StravaApi:
    def __init__(self, user):
        strava_login = user.social_auth.get(provider='strava')
        self.access_token = strava_login.extra_data['access_token']
        self.engine = create_engine(settings.ENGINE_URL)

    # def get_user(self):
    #     x = 1

    def store_activities(self, width = 0.001):
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
                width = 0.001

                for ind, row in prepped_df.iterrows():
                    for lat, long in row['polylines']:
                        user_ids.append(row['user_id'])
                        activities_ids.append(row['activity_id'])
                        lats.append(lat)
                        longs.append(long)
                        times.append(row['start_date_utc'])

                times = pd.to_datetime(times, utc=True)

                user_grid_df = pd.DataFrame(
                    {'activity_id': activities_ids, 'userID': user_ids, 'latitude': lats, 'longitude': longs,
                     'time': times})

                user_grid_df['grid_lat'] = round((user_grid_df['latitude'] + 90) / width).astype('int64')
                user_grid_df['grid_long'] = round((user_grid_df['longitude'] + 180) / width).astype('int64')
                tupled_df = pd.read_sql('SELECT * FROM \"painting_app_allgriddata\"', self.engine)
                full_grid_df = tupled_df_to_full_grid(tupled_df)
                full_grid_df['time'] = pd.to_datetime(full_grid_df['time'], utc=True)
                new_grid_df = pd.concat([user_grid_df, full_grid_df]).drop_duplicates()

                # canvas_df = pd.DataFrame(new_grid_df.sort_values('time').groupby(['grid_lat', 'grid_long']).last()).reset_index()
                # canvas_df = canvas_df[
                #     ['activity_id', 'userID', 'latitude', 'longitude', 'time', 'grid_lat', 'grid_long']]

                new_activities = (~user_grid_df['activity_id'].isin(full_grid_df['activity_id'])).sum()
                if new_activities != 0:
                    print(new_grid_df)
                    new_tupled_df = full_grid_to_tupled_df(new_grid_df)
                    print(new_tupled_df)
                    new_tupled_df.to_sql("painting_app_allgriddata", self.engine, if_exists='replace', index=False)
                    # canvas_df.to_sql("painting_app_canvasgriddata", self.engine, if_exists='replace', index=False)
                return new_activities

            prepped_df = prep_activities_df(activities_df)
            new_activities = prepped_to_sql(prepped_df)
            return new_activities
        new_activities = clean_data(activities_df)
        return new_activities

    def get_user_data(self):
        user_url = "https://www.strava.com/api/v3/athlete"

        access_token = self.access_token

        header = {'Authorization': 'Bearer ' + access_token}

        user_json = requests.get(user_url, headers=header).json()
        user_data = pd.json_normalize(user_json)

        current_users_df = pd.read_sql('SELECT * FROM \"painting_app_users\"', self.engine)


        if not user_data['id'][0] in current_users_df['id'].tolist():
            clr = random.choice(settings.COLOURS)
            user_data['color'] = clr
            user_data = user_data[['id','username','firstname','lastname','sex','city','state','country','color']]
            current_users_df = pd.concat([current_users_df,user_data])
            print('first path')

        else:
            clr = current_users_df['color'].loc[current_users_df['id'] == user_data['id'][0]]
            user_data['color'] = clr
            user_data = user_data[['id', 'username', 'firstname', 'lastname', 'sex', 'city', 'state', 'country', 'color']]
            current_users_df.loc[current_users_df['id'] == user_data['id'][0], :] = user_data
            print('second path')
        print(current_users_df)
        current_users_df.to_sql("painting_app_users", self.engine, if_exists='replace', index=False)
