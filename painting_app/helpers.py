import pandas as pd

def full_grid_to_tupled_df(full_grid_df):
    full_grid_df['time'] = full_grid_df['time'].apply(lambda x: x.value)
    tupled_df = pd.DataFrame({'tuple': [str(full_grid_df.apply(tuple, axis=1).tolist())]})
    return tupled_df

def tupled_df_to_full_grid(tupled_df):
    print(tupled_df)
    if tupled_df.empty:
        full_grid_df = pd.DataFrame(
            {'activity_id': None, 'userID': None, 'latitude': None, 'longitude': None, 'time': None, 'grid_lat': None,
             'grid_long': None}, index = [])
    elif (str(tupled_df['tuple'][0]) == '{}') or (str(tupled_df['tuple'][0]) == []): # inputted df is empty
        full_grid_df = pd.DataFrame(
            {'activity_id': None, 'userID': None, 'latitude': None, 'longitude': None, 'time': None, 'grid_lat': None,
             'grid_long': None}, index = [])
    else:
        cols = ['activity_id', 'userID', 'latitude', 'longitude', 'time', 'grid_lat',
                'grid_long']
        full_grid_df = pd.DataFrame(eval(tupled_df['tuple'][0]), columns=cols)
        full_grid_df['time'] = full_grid_df['time'].apply(pd.Timestamp)


    return full_grid_df

def full_grid_to_canvas_df(full_grid_df):
    canvas_df = pd.DataFrame(full_grid_df.sort_values('time').groupby(['grid_lat', 'grid_long']).last()).reset_index()
    return canvas_df
