from pathlib import Path
import pickle
import json
import numpy as np


__json_file_path = Path('columns.json').resolve()
__pkl_file_path = Path('banglore_home_prices_model.pickle').resolve()


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
        return ['nothing_n1']
    

def get_data_columns():
    f_json = open(__json_file_path)
    data_columns = json.load(f_json)['data_columns']
    f_json.close()
    return data_columns

def get_json_path():
    return str(__json_file_path)

if __name__ == '__main__':
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar',1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2)) # other location
    print(get_estimated_price('Ejipura', 1000, 2, 2))  # other location