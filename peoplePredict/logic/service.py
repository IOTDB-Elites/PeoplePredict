# -*- coding: utf-8 -*-
# constant
import datetime
from peoplePredict.database.dao import Dao
from peoplePredict.model.util.dao_service_util import build_position_to_name

INVALID = 0
CURRENT = 1
PREDICT = 2

HOUR = 0
DAY = 1
WEEK = 2

INTEGRATION_DATABASE = 'integrated_result'
DUMP_DATA_FILE = './peoplePredict/model/data/dao_service/position_name_map.pkl'

# env
dao = Dao()
position_name = build_position_to_name(DUMP_DATA_FILE)


# interface
def get_map_data(month, day, hour, aggregate):
    status = check_is_valid(month, day, hour)

    if status == INVALID:
        return build_error_resp(
            'Invalid date param. Month: ' + str(month) + ' day: ' + str(day) + ' hour: ' + str(hour))

    # if status == CURRENT:
    res = get_aggregate_position(month, day, hour, aggregate)

    if len(res) == 0:
        return build_error_resp(
            'Invalid aggregate param. aggregate: ' + str(aggregate))

    return {'success': True,
            'data': res}


def get_radius_data(month, day, hour, lng, lat, radius, aggregate):
    status = check_is_valid(month, day, hour)

    if status == INVALID:
        return build_error_resp(
            'Invalid date param. Month: ' + str(month) + ' day: ' + str(day) + ' hour: ' + str(hour))

    total_count = 0
    min_lat, max_lat, min_lng, max_lng = get_around(lat, lng, radius)
    if aggregate == HOUR:
        for row in dao.read_data_from_target_database(INTEGRATION_DATABASE, {'month': month,
                                                                             'day': day,
                                                                             'hour': hour,
                                                                             'lng_gcj02': {'$gt': min_lng,
                                                                                           '$lt': max_lng},
                                                                             'lat_gcj02': {'$gt': min_lat,
                                                                                           '$lt': max_lat}}):
            total_count += row['value']
    elif aggregate == DAY:
        # 按天聚合查询
        for row in dao.read_data_from_target_database(INTEGRATION_DATABASE, {'month': month,
                                                                             'day': day,
                                                                             'lng_gcj02': {'$gt': min_lng,
                                                                                           '$lt': max_lng},
                                                                             'lat_gcj02': {'$gt': min_lat,
                                                                                           '$lt': max_lat}}):
            total_count += row['value']
    elif aggregate == WEEK:
        # 按周聚合查询
        for row in dao.read_data_from_target_database(INTEGRATION_DATABASE, {'$or': build_week_filter(month, day),
                                                                             'lng_gcj02': {'$gt': min_lng,
                                                                                           '$lt': max_lng},
                                                                             'lat_gcj02': {'$gt': min_lat,
                                                                                           '$lt': max_lat}}):
            total_count += row['value']
    else:
        return build_error_resp(
            'Invalid aggregate param. aggregate: ' + str(aggregate))

    return {'success': True,
            'data': total_count}


def get_point_data(month, day, hour, lng, lat, aggregate):
    status = check_is_valid(month, day, hour)

    if status == INVALID:
        return build_error_resp(
            'Invalid date param. Month: ' + str(month) + ' day: ' + str(day) + ' hour: ' + str(hour))

    cur_date = datetime.date(2019, month, day)
    cur_date -= datetime.timedelta(days=3)
    res = []
    for i in range(7):
        num = 0
        month = cur_date.month
        day = cur_date.day
        if aggregate == HOUR:
            for row in dao.read_data_from_target_database(INTEGRATION_DATABASE, {'month': month,
                                                                                 'day': day,
                                                                                 'hour': hour,
                                                                                 'lng_gcj02': round(float(lng), 3),
                                                                                 'lat_gcj02': round(float(lat), 3)}):
                num += row['value']
        elif aggregate == DAY:
            # 按照天聚合
            for row in dao.read_data_from_target_database(INTEGRATION_DATABASE, {'month': month,
                                                                                 'day': day,
                                                                                 'lng_gcj02': round(float(lng), 3),
                                                                                 'lat_gcj02': round(float(lat), 3)}):
                num += row['value']
        else:
            return build_error_resp(
                'Invalid aggregate param. aggregate: ' + str(aggregate))

        res.append({'month': month, 'day': day, 'val': num})
        cur_date += datetime.timedelta(days=1)

    return {'success': True,
            'data': res}


def get_top_ten_street(month, day, hour, aggregate):
    status = check_is_valid(month, day, hour)

    if status == INVALID:
        return build_error_resp(
            'Invalid date param. Month: ' + str(month) + ' day: ' + str(day) + ' hour: ' + str(hour))

    res = get_aggregate_position(month, day, hour, aggregate)

    if len(res) == 0:
        return build_error_resp(
            'Invalid aggregate param. aggregate: ' + str(aggregate))

    res.sort(key=lambda x: x['val'], reverse=True)

    out = []
    for i in range(10):
        cur = res[i]
        key = build_key_by_lng_lat(cur['lng'], cur['lat'])
        name = position_name.get(key, '未知地点')
        out.append({'name': name,
                    'val': cur['val']})

    return {'success': True,
            'data': out}


# helper
import math

PI = 3.14159265
EARTH_RADIUS = 6378137
RAD = PI / 180.0
DEGREE = (24901 * 1609) / 360.0


# get around latitude and longitude
def get_around(lat, lng, radius):
    latitude = lat
    longitude = lng
    radius_mile = radius
    # latitude
    dpm_lat = 1 / DEGREE
    radius_lat = dpm_lat * radius_mile
    min_lat = latitude - radius_lat
    max_lat = latitude + radius_lat
    # longitude
    mpd_lng = DEGREE * math.cos(latitude * (PI / 180))
    dpm_lng = 1 / mpd_lng
    radius_lng = dpm_lng * radius_mile
    min_lng = longitude - radius_lng
    max_lng = longitude + radius_lng

    return min_lat, max_lat, min_lng, max_lng


# check whether the date is valid
def check_is_valid(month, day, hour):
    if hour not in [7, 12, 15, 20, 21]:
        return INVALID

    if month == 8:
        return CURRENT if 20 <= day <= 31 else INVALID

    if month == 9:
        if day > 30:
            return INVALID
        return CURRENT if day <= 23 else PREDICT

    return INVALID


def build_error_resp(message='Unknown internal error'):
    return {'success': False,
            'message': message}


def build_key(row):
    return str(row['lng_gcj02']) + ',' + str(row['lat_gcj02'])


def build_key_by_lng_lat(lng, lat):
    return str(lng) + ',' + str(lat)


def to_data(key):
    lng, lat = key.split(',')
    return round(float(lng), 3), round(float(lat), 3)


# 寻找指定聚合方式下，指定月，指定天，指定小时的所有点的聚合值
def get_aggregate_position(month, day, hour, aggregate):
    res = []
    if aggregate == HOUR:
        for row in dao.read_data_from_target_database(INTEGRATION_DATABASE, {'month': month,
                                                                             'day': day,
                                                                             'hour': hour}):
            res.append({'lng': row['lng_gcj02'], 'lat': row['lat_gcj02'], 'val': row['value']})
    elif aggregate == DAY:
        # 按天聚合查询
        aggregate_map = {}
        for row in dao.read_data_from_target_database(INTEGRATION_DATABASE, {'month': month,
                                                                             'day': day}):
            key = build_key(row)
            if key in aggregate_map:
                aggregate_map[key] += row['value']
            aggregate_map[key] = row['value']
        for key in aggregate_map:
            lng, lat = to_data(key)
            res.append({'lng': lng, 'lat': lat, 'val': aggregate_map[key]})
    elif aggregate == WEEK:
        # 按周聚合查询
        aggregate_map = {}
        for row in dao.read_data_from_target_database(INTEGRATION_DATABASE, {'$or': build_week_filter(month, day)}):
            key = build_key(row)
            aggregate_map[key] = aggregate_map.get(key, 0) + row['value']

        for key in aggregate_map:
            lng, lat = to_data(key)
            res.append({'lng': lng, 'lat': lat, 'val': aggregate_map[key]})
    return res


def build_week_filter(month, day):
    cur_date = datetime.date(2019, month, day)
    cur_date -= datetime.timedelta(days=3)
    res = []
    for i in range(7):
        month = cur_date.month
        day = cur_date.day
        res.append({'month': month, 'day': day})
        cur_date += datetime.timedelta(days=1)

    return res


if __name__ == '__main__':
    print(get_around(108.786, 34.335, 1000))
