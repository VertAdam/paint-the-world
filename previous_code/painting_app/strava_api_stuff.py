import json
import requests
import urllib3
import pandas as pd
import polyline
import helpers

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class StravaAPI():
    def __init__(self, codes_path):
        with open(codes_path, 'r') as f:
            self.codes = json.load(
                f)  # TODO: NEED TO USE social_django.models.UserSocialAuth to get the Strava login for all users

    def get_user_dict(self):
        auth_url = "https://www.strava.com/oauth/token"
        user_url = "https://www.strava.com/api/v3/athlete"

        # Get access token
        print("Requesting Token...\n")
        res = requests.post(auth_url, data=self.codes, verify=False)
        access_token = res.json()['access_token']
        print("Access Token = {}\n".format(access_token))

        # Get activity data
        header = {'Authorization': 'Bearer ' + access_token}
        activity_df_list = []

        user_dict = requests.get(user_url, headers=header).json()
        prepped_user_dict = helpers.prep_user_dict(user_dict) # TODO: Need to do a check where colour is chosen if the user has already selected a colour previously
        print('Imported', len(activities_df), 'activities')

        return user_dict

    def get_activities(self):

        auth_url = "https://www.strava.com/oauth/token"
        activites_url = "https://www.strava.com/api/v3/athlete/activities"

        # Get access token
        print("Requesting Token...\n")
        res = requests.post(auth_url, data=self.codes, verify=False)
        access_token = res.json()['access_token']
        print("Access Token = {}\n".format(access_token))

        # Get activity data
        header = {'Authorization': 'Bearer ' + access_token}
        activity_df_list = []
        for n in range(5):  # TODO: Change this to be higher
            param = {'per_page': 200, 'page': n + 1}

            activities_json = requests.get(activites_url, headers=header, params = param).json()
            if not activities_json:
                break
            activity_df_list.append(pd.json_normalize(activities_json))
        activities_df = pd.concat(activity_df_list)
        print('Imported', len(activities_df), 'activities')

        return activities_df

    def prep_df(self, activities_df):
        activities_df['polylines'] = activities_df['map.summary_polyline']
        prepped_activities_df = activities_df[['type', 'start_date_local', 'timezone', 'polylines']]
        prepped_activities_df = prepped_activities_df.dropna(subset=['polylines'])
        prepped_activities_df['polylines'] = prepped_activities_df['polylines'].apply(polyline.decode)
        prepped_activities_df = prepped_activities_df.reset_index(drop=True)
        return prepped_activities_df





if __name__ == "__main__":
    s = StravaAPI(r'C:\Users\verta\PycharmProjects\paint-the-world\codes.json')
    activities_df = s.get_activities()
    user_df = s.get_user_data()



