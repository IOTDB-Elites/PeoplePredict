from pymongo import MongoClient
from peoplePredict.database.constant import port, uri, people_num_database, poi_database, join_database


def build_location_list(poi_l):
    # 经度
    longitude_l = []
    # 纬度
    latitude_l = []
    for poi in poi_l:
        pair = poi['location'].split(",")
        longitude_l.append(float(pair[0]))
        latitude_l.append(float(pair[1]))

    return longitude_l, latitude_l


def cal_distance(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def found_nearest(longitude_l, latitude_l, lng, lat):
    loc = 0
    dis = cal_distance(longitude_l[0], latitude_l[0], lng, lat)
    for i in range(1, len(longitude_l)):
        cur_dis = cal_distance(longitude_l[0], latitude_l[0], lng, lat)
        if cur_dis < dis:
            loc = i
            dis = cur_dis

    return loc


if __name__ == '__main__':
    # build connection
    conn = MongoClient(uri, port=port)
    db = conn.qh_area_forecast
    people_num_set = db[people_num_database]
    poi_set = db[poi_database]

    # data in memory
    count = 0
    people_l = []
    poi_l = []

    for i in people_num_set.find():
        people_l.append(i)
        count += 1
        if count % 1000 == 500:
            print(count)

    count = 0
    for i in poi_set.find():
        poi_l.append(i)
        count += 1
        if count % 1000 == 0:
            print(count)

    # find nearest poi
    longitude, latitude = build_location_list(poi_l)
    count = 0
    cache = {}
    for location in people_l:
        key = str(location['lng_gcj02']) + ',' + str(location['lat_gcj02'])
        if key not in cache:
            lng = location['lng_gcj02']
            lat = location['lat_gcj02']
            loc = found_nearest(longitude, latitude, lng, lat)
            # update cache
            cache[key] = loc
        else:
            loc = cache[key]

        location.update(poi_l[loc])
        location.pop('_id')
        count += 1
        if count % 1000 == 0:
            print(count)

    # insert preprocessed data
    people_num_join_poi = db[join_database]

    people_num_join_poi.delete_many({})
    cache = []
    count = 0
    for location in people_l:
        location['lng_gcj02'] = round(location['lng_gcj02'], 3)
        location['lat_gcj02'] = round(location['lat_gcj02'], 3)
        cache.append(location)
        if len(cache) == 100:
            people_num_join_poi.insert_many(cache)
            cache.clear()
            count += 1
            print(count * 100)
    if len(cache) != 0:
        people_num_join_poi.insert_many(cache)

    conn.close()
