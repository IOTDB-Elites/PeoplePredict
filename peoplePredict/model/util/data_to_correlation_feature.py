from peoplePredict.database.dao import Dao
import numpy as np
import os

DUMP_FILE = '../data/correlation_model/matrix'


def to_loc(month, day):
    if month == 8:
        return day - 20
    return 11 + day


def build_matrix_in_hour(hour):
    dao = Dao()
    # (lat, lng) -> [val]
    location_array = {}

    for row in dao.read_data({'hour': hour}):
        key = str(row['lng_gcj02']) + ',' + str(row['lat_gcj02'])
        loc = to_loc(row['month'], row['day'])
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
        for i in range(35):
            if i in cur_map:
                cur_array.append(cur_map[i])
            else:
                cur_array.append(0)
        res.append((key, cur_array))
        location.append(key)

    res.sort(key=lambda x: x[0])
    location.sort()

    matrix = np.zeros((len(res), 35))
    for i in range(len(res)):
        matrix[i] = np.array(res[i][1])

    return matrix, location


def build_matrix():
    if os.path.exists(DUMP_FILE + ".npz"):
        zip_file = np.load(DUMP_FILE + ".npz", allow_pickle=True)
        return zip_file['matrix'], zip_file['location']

    print("we don't have dump data. build from script, please wait...")
    m_list = []
    loc_list = []
    for hour in [7, 12, 15, 20, 21]:
        matrix, location = build_matrix_in_hour(hour)
        m_list.append(matrix)
        loc_list.append(location)
        print(hour, " done!")

    np.savez(DUMP_FILE, matrix=m_list, location=loc_list)
    return m_list, loc_list


if __name__ == '__main__':
    m, l = build_matrix()
    print(m[0].shape, len(l[0]), l[0][0])
