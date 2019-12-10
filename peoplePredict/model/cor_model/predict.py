import os

import numpy as np

from peoplePredict.database.dao import Dao
from peoplePredict.model.util import data_to_correlation_feature as data_load

DUMP_FILE = '../data/correlation_model/7days'


def to_loc(day):
    return day - 24


def build_matrix_in_hour(hour):
    dao = Dao()
    # (lat, lng) -> {loc -> val}
    location_array = {}

    for row in dao.read_data_from_target_databse('poi_model_result', {'hour': hour}):
        key = str(row['lng_gcj02']) + ',' + str(row['lat_gcj02'])
        loc = to_loc(row['day'])
        if key in location_array:
            location_array[key][loc] = row['value']
        else:
            location_array[key] = {loc: row['value']}

    print("load data finished!")
    res = []
    location = {}
    id = 0
    for key in location_array:
        cur_map = location_array[key]
        cur_array = []
        for i in range(7):
            if i in cur_map:
                cur_array.append(cur_map[i])
            else:
                cur_array.append(0)
        res.append((key, cur_array))
        location[key] = id
        id += 1

    matrix = np.zeros((len(res), 7))
    for i in range(len(res)):
        matrix[i] = np.array(res[i][1])

    dao.close()
    return matrix, location


def build_matrix():
    if os.path.exists(DUMP_FILE + ".npz"):
        zip_file = np.load(DUMP_FILE + ".npz", allow_pickle=True)
        return zip_file['matrix'], zip_file['location']

    print("we don't have dump data. build from script, please wait...")
    m_list = []
    loc_list = []
    matrix, location = build_matrix_in_hour(7)
    m_list.append(matrix)
    loc_list.append(location)
    print(" done!")
    # for hour in [7, 12, 15, 20, 21]:
    #     matrix, location = build_matrix_in_hour(hour)
    #     m_list.append(matrix)
    #     loc_list.append(location)
    #     print(hour, " done!")

    np.savez(DUMP_FILE, matrix=m_list, location=loc_list)
    return np.array(m_list)[0], np.array(loc_list)


def get_first():
    return []


# def predict(prev, index_list, parameter_list):
#     return ((prev[index_list].T * parameter_list[:,0]) + parameter_list[:,1].T).T.astype(np.int32)






def merge(a, b):
    if a.shape[0] == 0:
        return b
    elif b.shape[0] == 0:
        return a
    else:
        return np.c_[a, b]


def predict(data1, datamap, model_index_list, m_prev_index_list1, m_prev_index_list2,model_parameter_k, model_parameter_b):
    p1 = np.zeros((len(m_prev_index_list1), 7))

    for i in range(0, p1.shape[0]):
        p1[i] = data1[datamap[m_prev_index_list1[i]]]

    t = np.zeros((model_index_list.shape[0], 7))
    for i in range(0, model_index_list.shape[0]):
        t[i] = p1[model_index_list[i]]

    res1 = (t.T*model_parameter_k + model_parameter_b).T
    res1 = np.where(res1 > 0, res1, 0)
    map1 = {}
    for i in range(0, len(m_prev_index_list2)):
        map1[m_prev_index_list2[i]] = i
    return res1.astype('int32'), map1

def upload_data(matrix, map):
    DATABASE = 'correlation_model_result'
    dao = Dao()
    cache = []
    count = 0
    # dao.clear_database(DATABASE)
    hour_list = [7, 12, 15, 20, 21]

    for i in range(0, len(matrix)):
        time_matrix = matrix[i]
        time_map = map[i]
        base_month = 9
        base_day = 24
        hour = hour_list[i]
        for j in time_map:
            lng, lat = str(j).split(',')
            for k in range(0, 7):
                item = {
                    'month': base_month,
                    'day': base_day + k,
                    'hour': hour,
                    'lng_gcj02': lng,
                    'lat_gcj02': lat,
                    'value': time_matrix[time_map[j]][k]
                }
                print(item)
                cache.append(item)

                if len(cache) == 100:
                    count += 100
                    dao.insert_many(DATABASE, cache)
                    cache.clear()
                    if count % 1000 == 0:
                        print(count)
        if len(cache) != 0:
            dao.insert_many(DATABASE, cache)
        dao.close()




# dao.clear_database(DATABASE)
# for row in your_data:
#     cache.append({'month': 10,
#                   'day': row[0],
#                   'hour': row[1],
#                   'lng_gcj02': row[2],
#                   'lat_gcj02': row[3],
#                   'value': row[4])})
#
#     if len(cache) == 100:
#         count += 100
#         dao.insert_many(DATABASE, cache)
#         cache.clear()
#         if count % 1000 == 0:
#             print(count)
#             if len(cache) != 0:
# if len(cache) != 0:
#     dao.insert_many(DATABASE, cache)
# dao.close()

if __name__ == '__main__':
    model_index = np.load("../data/correlation_model/model_max_index.npy", allow_pickle=True)
    model_parameter = np.load("../data/correlation_model/model_parameter.npy", allow_pickle=True)
    m_prev, l_prev = data_load.build_matrix()
    first_time, map = build_matrix()
    first_time = first_time[0]
    map = map[0]

    # print(model_parameter[0][:,0].shape)

    # print(l_prev[0])

    res1, mp1 = predict(first_time, map, model_index[0], l_prev[0], l_prev[1],model_parameter[0][:,0], model_parameter[0][:,1])
    res2, mp2 = predict(res1, mp1, model_index[1], l_prev[1], l_prev[2], model_parameter[1][:, 0],
                        model_parameter[1][:, 1])
    res3, mp3=  predict(res2, mp2, model_index[2], l_prev[2], l_prev[3], model_parameter[2][:, 0],
                        model_parameter[2][:, 1])
    res4, mp4= predict(res3, mp3, model_index[3], l_prev[3], l_prev[4], model_parameter[3][:, 0],
                        model_parameter[3][:, 1])

    result = [first_time, res1, res2, res3, res4]
    result_map = [map, mp1, mp2,mp3, mp4]

    upload_data(result, result_map)




    # print(res2)
    #
    # p1 = np.zeros((m_prev[0].shape[0], 7))
    #
    # for i in range(0, p1.shape[0]):
    #     p1[i] = first_time[map[l_prev[0][i]]]
    #
    # t = np.zeros((model_index[0].shape[0], 7))
    # for i in range(0, model_index[0].shape[0]):
    #     t[i] = p1[model_index[0][i]]
    #
    # res1 = (t.T*model_parameter[0][:,0] + model_parameter[0][:,1]).T
    # res1 = np.where(res1 > 0, res1, 0)
    # map1 = {}
    # for i in range(0, len(l_prev[1])):
    #     map1[l_prev[1][i]] = i





    #
    #
    #
    # print(first_time.shape)
    # print(model_index)
    # print(model_index[0].shape)
    # print(model_index[1].shape)
    # print(model_index[2].shape)
    # print(model_index[3].shape)

    # print(model_parameter)




    # print(m_prev[0].shape)
    # print(m_prev[1].shape)
    # print(m_prev[2].shape)
    # print(m_prev[3].shape)
    # print(m_prev[4].shape)
