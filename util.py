from pathlib import Path
import pickle
import json
import numpy as np
import os

__locations = None
__data_columns = None
__model = None
__json_file_path = Path('columns.json').resolve()
__pkl_file_path = Path('banglore_home_prices_model.pickle').resolve()


def get_estimated_price(location,sqft,bhk,bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2)


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __locations

    f_json = open(__json_file_path)
    __data_columns = json.load(f_json)['data_columns']
    __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk
    f_json.close()

    global __model
    if __model is None:

        f_pkl = open(__pkl_file_path,'rb')
        __model = pickle.load(f_pkl)
        f_pkl.close()

    print("loading saved artifacts...done")

def get_location_names():
    try:
        f_json = open(__json_file_path)
        data_columns = json.load(f_json)['data_columns']
        locations = data_columns[3:]  # first 3 columns are sqft, bath, bhk
        return locations
    except:
        return ['nothing_n1']
    

def get_data_columns():
    return __data_columns

def get_json_path():
    return str(__json_file_path)

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar',1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2)) # other location
    print(get_estimated_price('Ejipura', 1000, 2, 2))  # other location