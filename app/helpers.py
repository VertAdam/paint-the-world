import polyline
import random
def prep_activities_df(activities_df):
    # Cleans up the dataframe returned from StravaAPI().get_activities()
    activities_df['polylines'] = activities_df['map.summary_polyline']
    prepped_activities_df = activities_df[['type', 'start_date_local', 'timezone', 'polylines']]
    prepped_activities_df = prepped_activities_df.dropna(subset=['polylines'])
    prepped_activities_df['polylines'] = prepped_activities_df['polylines'].apply(polyline.decode)
    prepped_activities_df = prepped_activities_df.reset_index(drop=True)
    return prepped_activities_df

def prep_user_dict(user_dict, colour = None):
    # Cleans up the user data dictionary returned from StravaAPI().get_user_data()
    keys = ['id', 'username', 'firstname', 'lastname','city','state','country','sex']
    prepped_user_dict = {key: user_dict[key] for key in keys}

    with open('app/data/colors.txt', 'r') as f:
        allowed_colours = f.read().splitlines()

    if colour is None:
        prepped_user_dict['colour'] = random.choice(allowed_colours)
    else:
        colour = colour.lower()
        if colour not in allowed_colours:
            raise AttributeError('Colour chosen is not one of the allowed colours')
        prepped_user_dict['colour'] = colour
    return prepped_user_dict


