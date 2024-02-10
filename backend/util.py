from pathlib import Path
import pickle
import json
import numpy as np


__json_file_path = Path('backend/artifacts/columns.json').resolve()
__pkl_file_path = Path('backend/artifacts/banglore_home_prices_model.pickle').resolve()


def get_estimated_price(location,sqft,bhk,bath):
    f_json = open(__json_file_path)
    data_columns = json.load(f_json)['data_columns']
    f_json.close()    

    try:
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1

    f_pkl = open(__pkl_file_path,'rb')
    model = pickle.load(f_pkl)
    f_pkl.close()

    return round(model.predict([x])[0],2)


def get_location_names():
    try:
        f_json = open(__json_file_path)
        data_columns = json.load(f_json)['data_columns']
        locations = data_columns[3:]  # first 3 columns are sqft, bath, bhk
        f_json.close()
        return locations
    except:
        return ['empty_list']
    

def get_data_columns():
    f_json = open(__json_file_path)
    data_columns = json.load(f_json)['data_columns']
    f_json.close()
    return data_columns