from peoplePredict.database.dao import Dao
import numpy as np
import os

DUMP_FILE = '../data/arima_model/matrix'

hour_map = {7: 0, 12: 1, 15: 2, 20: 3, 21: 4}


def to_loc(month, day, hour):
    if month == 8:
        return (day - 20) * 5 + hour_map[hour]
    return (11 + day) * 5 + hour_map[hour]


def build_matrix_all_hours():
    dao = Dao()
    location_array = {}

    for row in dao.read_data():
        key = str(row['lng_gcj02']) + ',' + str(row['lat_gcj02'])
        loc = to_loc(row['month'], row['day'], row['hour'])
        if key in location_array:
            location_array[key][loc] = row['value']
        else:
            location_array[key] = {loc: row['value']}

    print("load data finished!")
    res = []
    location = []
    for key in location_array:
        cur_map = location_array[key]
        cur_array = []
        for i in range(35*5):
            if i in cur_map:
                cur_array.append(cur_map[i])
            else:
                cur_array.append(0)
        res.append((key, cur_array))
        location.append(key)

    matrix = np.zeros((len(res), 35*5))
    for i in range(len(res)):
        matrix[i] = np.array(res[i][1])

    return matrix, location


def build_matrix():
    if os.path.exists(DUMP_FILE + ".npz"):
        zip_file = np.load(DUMP_FILE + ".npz", allow_pickle=True)
        return zip_file['matrix'], zip_file['location']

    print("we don't have dump data. build from script, please wait...")

    matrix, location = build_matrix_all_hours()

    print("done!")

    np.savez(DUMP_FILE, matrix=matrix, location=location)
    return matrix, location


if __name__ == '__main__':
    m, l = build_matrix()
    print(m[8888], len(l), l[0])
