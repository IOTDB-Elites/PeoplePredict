import numpy as np
import os
import pickle

from peoplePredict.database.dao import Dao

DUMP_FILE = '../data/dao_service/position_name_map.pkl'


def build_position_to_name(file_name=None):
    if file_name is None:
        file_name = DUMP_FILE

    print(os.path.abspath(file_name))
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            return pickle.load(file)

    print("we don't have dump data. build from script, please wait...")
    dao = Dao()

    position_name_map = {}
    count = 0
    for row in dao.read_data():
        key = str(row['lng_gcj02']) + ',' + str(row['lat_gcj02'])
        position_name_map[key] = row['name']
        count += 1
        if count % 1000 == 0:
            print(count)

    with open(DUMP_FILE, 'wb') as file:
        pickle.dump(position_name_map, file)

    dao.close()
    return position_name_map


if __name__ == '__main__':
    build_position_to_name()
