import numpy as np
import os

from peoplePredict.database.dao import Dao

DUMP_FILE = '../data/dao_service/position_name_map'


def build_position_to_name():
    if os.path.exists(DUMP_FILE + ".npz"):
        zip_file = np.load(DUMP_FILE + ".npz", allow_pickle=True)
        return zip_file['map']

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

    np.savez(DUMP_FILE, map=position_name_map)

    dao.close()
    return position_name_map
