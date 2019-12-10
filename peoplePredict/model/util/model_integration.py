from peoplePredict.database.dao import Dao
from peoplePredict.model.util.dao_service_util import build_position_to_name

POI_DATABASE = 'poi_model_result'
ARIMA_DATABASE = 'arima_model_result'
CORRELATION_DATABSE = 'correlation_model_result'
INTEGRATION_DATABASE = 'integrated_result'


# helper method
def build_key(row):
    return str(row['lng_gcj02']) + ',' + str(row['lat_gcj02']) + ',' + str(row['day']) + ',' + str(row['hour'])


def read_data_from_database(dao, ratio, res_map, database_name):
    for row in dao.read_data_from_target_database(database_name):
        key = build_key(row)
        val = 0
        if key in res_map:
            val += res_map[key]
        res_map[key] = val + row['value'] * ratio
    print("finish reading database: ", database_name)


# main method
def model_integration(ratio=(0.333, 0.333, 0.333)):
    print('model integration')

    dao = Dao()

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
                      'day': int(col[2]),
                      'hour': int(col[3]),
                      'lng_gcj02': round(float(col[0]), 3),
                      'lat_gcj02': round(float(col[1]), 3),
                      'name': position_name_map(col[0] + ',' + col(1)),
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


if __name__ == '__main__':
    print('begin integration')
    current_data_integration()
    # model_integration()
    print('integration ends')
