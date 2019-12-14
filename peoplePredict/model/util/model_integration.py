from peoplePredict.database.dao import Dao
from peoplePredict.model.util.dao_service_util import build_position_to_name

POI_DATABASE = 'poi_model_result'
ARIMA_DATABASE = 'arima_model_result'
CORRELATION_DATABSE = 'correlation_model_result'
INTEGRATION_DATABASE = 'integrated_result'
VIEW_DATABASE = 'view_result'


# helper method
def build_key(row):
    return str(row['lng_gcj02']) + ',' + str(row['lat_gcj02']) + ',' + str(int(float(row['day']))) + ',' + str(
        int(float(row['hour'])))


def read_data_from_database(dao, ratio, res_map, database_name):
    count = 0
    for row in dao.read_data_from_target_database(database_name):
        count += 1
        key = build_key(row)
        val = 0
        if key in res_map:
            val += res_map[key]
        res_map[key] = val + row['value'] * ratio
    print("finish reading database: ", database_name)
    print("total data point: ", count)


# main method
def model_integration(ratio=(0.333, 0.333, 0.333)):
    print('model integration')

    dao = Dao()
    # clear database
    count = dao.clear_database(INTEGRATION_DATABASE, {'month': 9, 'day': {'$gt': 23}})
    print('clear count: ', count)
    #

    position_name_map = build_position_to_name()
    res_map = {}
    # read data base
    read_data_from_database(dao, ratio[0], res_map, POI_DATABASE)
    read_data_from_database(dao, ratio[1], res_map, ARIMA_DATABASE)
    read_data_from_database(dao, ratio[2], res_map, CORRELATION_DATABSE)

    # insert into databse
    print('inserting into final database')
    cache = []
    count = 0
    for key in res_map:
        col = key.split(',')
        cache.append({'month': 9,
                      'day': int(float(col[2])),
                      'hour': int(float(col[3])),
                      'lng_gcj02': round(float(col[0]), 3),
                      'lat_gcj02': round(float(col[1]), 3),
                      'name': position_name_map[col[0] + ',' + col[1]],
                      'value': int(res_map[key])})
        if len(cache) == 100:
            count += 100
            dao.insert_many(INTEGRATION_DATABASE, cache)
            cache.clear()
            if count % 10000 == 0:
                print(count)
    if len(cache) != 0:
        dao.insert_many(INTEGRATION_DATABASE, cache)

    dao.close()


def current_data_integration():
    dao = Dao()
    # clear database
    dao.clear_database(INTEGRATION_DATABASE)
    # insert into databse
    print('transfer current data into final database')
    cache = []
    count = 0
    for row in dao.read_data():
        cache.append({'month': row['month'],
                      'day': row['day'],
                      'hour': row['hour'],
                      'lng_gcj02': round(float(row['lng_gcj02']), 3),
                      'lat_gcj02': round(float(row['lat_gcj02']), 3),
                      'name': row['name'],
                      'value': int(row['value'])})
        if len(cache) == 100:
            count += 100
            dao.insert_many(INTEGRATION_DATABASE, cache)
            cache.clear()
            if count % 10000 == 0:
                print(count)
    if len(cache) != 0:
        dao.insert_many(INTEGRATION_DATABASE, cache)

    dao.close()


# for view project
def find_top_position(top_count):
    dao = Dao()

    # read all data to build people count map
    res_map = {}
    count = 0
    for row in dao.read_data():
        count += 1
        key = str(row['lng_gcj02']) + ',' + str(row['lat_gcj02'])
        res_map[key] = res_map.get(key, 0) + row['value']
        if count % 10000 == 0:
            print(count)

    res_list = []
    for key in res_map:
        res_list.append((key, res_map[key]))

    # find top
    res_list.sort(key=lambda x: x[1], reverse=True)
    final_res = res_list[0:top_count]
    print(final_res)
    final_set = set()
    for row in final_res:
        final_set.add(row[0])

    print('write to view database')
    cache = []
    count = 0
    for row in dao.read_data_from_target_database(INTEGRATION_DATABASE):
        key = str(row['lng_gcj02']) + ',' + str(row['lat_gcj02'])
        if key in final_set:
            cache.append({'month': row['month'],
                          'day': row['day'],
                          'hour': row['hour'],
                          'lng_gcj02': round(float(row['lng_gcj02']), 3),
                          'lat_gcj02': round(float(row['lat_gcj02']), 3),
                          'name': row['name'],
                          'value': int(row['value'])})
            if len(cache) == 100:
                count += 100
                dao.insert_many(VIEW_DATABASE, cache)
                cache.clear()
                if count % 10000 == 0:
                    print(count)
    if len(cache) != 0:
        dao.insert_many(VIEW_DATABASE, cache)

    dao.close()


if __name__ == '__main__':
    print('begin integration')
    # current_data_integration()
    #  model_integration()
    find_top_position(1000)
    print('integration ends')
