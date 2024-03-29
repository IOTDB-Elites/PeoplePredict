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
DISTRICT_DATABASE = 'district_result'
DISTRICT_DATABASE_HOUR = 'district_result_hour'
DUMP_DATA_FILE = './peoplePredict/model/data/dao_service/position_name_map.pkl'

# env
dao = Dao()
position_name = build_position_to_name(DUMP_DATA_FILE)
pos_map = {7: 1,
           12: 2,
           15: 3,
           20: 4,
           21: 5}


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
    day_map = {}
    if aggregate == HOUR:
        for row in dao.read_data_from_target_database(INTEGRATION_DATABASE, {'$or': build_week_filter(month, day),
                                                                             'hour': hour,
                                                                             'lng_gcj02': {'$gt': min_lng,
                                                                                           '$lt': max_lng},
                                                                             'lat_gcj02': {'$gt': min_lat,
                                                                                           '$lt': max_lat}}):
            key = build_date_key(row)
            day_map[key] = day_map.get(key, 0) + row['value']
    elif aggregate == DAY:
        # 按天聚合查询
        for row in dao.read_data_from_target_database(INTEGRATION_DATABASE, {'$or': build_week_filter(month, day),
                                                                             'lng_gcj02': {'$gt': min_lng,
                                                                                           '$lt': max_lng},
                                                                             'lat_gcj02': {'$gt': min_lat,
                                                                                           '$lt': max_lat}}):
            key = build_date_key(row)
            day_map[key] = day_map.get(key, 0) + row['value']
    else:
        return build_error_resp(
            'Invalid aggregate param. aggregate: ' + str(aggregate))

    min_count = 1000000000
    max_count = 0
    num = 0
    res = []
    for key in day_map:
        cur_count = day_map[key]
        res.append({'month': key[0], 'day': key[1], 'val': cur_count})
        min_count = min(min_count, cur_count)
        max_count = max(max_count, cur_count)
        total_count += cur_count
        num += 1

    return {'success': True,
            'data': res,
            'statistic': {'min': min_count,
                          'max': max_count,
                          'avg': total_count / num,
                          'sum': total_count}}


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

        res.append({'month': month, 'day': day, 'count': num})
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

    res.sort(key=lambda x: x['count'], reverse=True)

    out = []
    for i in range(10):
        cur = res[i]
        key = build_key_by_lng_lat(cur['lng'], cur['lat'])
        name = position_name.get(key, '未知地点')
        out.append({'name': name,
                    'val': cur['count'],
                    'lng': cur['lng'],
                    'lat': cur['lat']})

    return {'success': True,
            'data': out}


def get_all_district(month, day):
    status = check_is_valid(month, day, 7)

    if status == INVALID:
        return build_error_resp(
            'Invalid date param. Month: ' + str(month) + ' day: ' + str(day))

    district_map = {}
    for row in dao.read_data_from_target_database(DISTRICT_DATABASE, {'month': month,
                                                                      'day': day}):
        key = row['adname']
        district_map[key] = district_map.get(key, 0) + row['value']

    list_for_sort = []
    for key in district_map:
        list_for_sort.append([key, district_map[key] // 5])
    list_for_sort.sort(key=lambda x: x[1], reverse=True)

    out = []
    for pair in list_for_sort:
        out.append({'name': pair[0],
                    'val': pair[1]})

    return {'success': True,
            'data': out}


def get_district_point(name):
    calendar_map = {}
    for row in dao.read_data_from_target_database(DISTRICT_DATABASE, {'adname': name}):
        calendar_key = (row['month'], row['day'])
        calendar_map[calendar_key] = calendar_map.get(calendar_key, 0) + row['value']

    # build calendar res
    calendar_res = []
    min_val = 10000000
    max_val = 0
    for key in calendar_map:
        pad = '-0' if key[1] // 10 == 0 else '-'
        val = calendar_map[key] // 5
        calendar_res.append(['2019-0' + str(key[0]) + pad + str(key[1]), val])
        min_val = min(min_val, val)
        max_val = max(max_val, val)

    return {'success': True,
            'calendar_res': calendar_res,
            'min_val': min_val,
            'max_val': max_val}


def get_district_line(name):
    res = [[], [], [], [], [], []]

    cur_date = datetime.date(2019, 8, 20)
    for i in range(35):
        res[0].append(cur_date.strftime('%Y-%m-%d'))
        for j in range(1, 6):
            res[j].append(0)
        cur_date += datetime.timedelta(days=1)

    for row in dao.read_data_from_target_database(DISTRICT_DATABASE_HOUR, {'adname': name}):
        loc = to_loc(row['month'], row['day'])
        print("!!!!")
        print(res[pos_map[row['hour']]][loc])
        res[pos_map[row['hour']]][loc] += row['value']

    return {'success': True,
            'res': res}


def get_district_treemap(name):
    total_map = {}
    for row in dao.read_data_from_target_database(DISTRICT_DATABASE, {'adname': name}):
        l = list(row['type'].split(';'))
        while len(l) < 3:
            l.append('其他')

        big, mid, small = l[0], l[1], l[2]
        if big not in total_map:
            total_map[big] = {}
        if mid not in total_map[big]:
            total_map[big][mid] = {}
        total_map[big][mid][small] = total_map[big][mid].get(small, 0) + row['value']

    res = []
    for big in total_map:
        big_children = []
        big_sum = 0
        for mid in total_map[big]:
            mid_children = []
            mid_sum = 0
            for small in total_map[big][mid]:
                val = total_map[big][mid][small]
                mid_children.append({'name': small,
                                     'value': val})
                mid_sum += val
                big_sum += val
            big_children.append({'name': mid,
                                 'value': mid_sum,
                                 'children': mid_children})
        res.append({'name': big,
                    'value': big_sum,
                    'children': big_children})

    return {'success': True,
            'data': res}


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


def build_date_key(row):
    return row['month'], row['day']


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
            res.append({'lng': row['lng_gcj02'], 'lat': row['lat_gcj02'], 'count': row['value']})
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
            res.append({'lng': lng, 'lat': lat, 'count': aggregate_map[key]})
    elif aggregate == WEEK:
        # 按周聚合查询
        aggregate_map = {}
        for row in dao.read_data_from_target_database(INTEGRATION_DATABASE, {'$or': build_week_filter(month, day)}):
            key = build_key(row)
            aggregate_map[key] = aggregate_map.get(key, 0) + row['value']

        for key in aggregate_map:
            lng, lat = to_data(key)
            res.append({'lng': lng, 'lat': lat, 'count': aggregate_map[key]})
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


def to_loc(month, day):
    if month == 8:
        return day - 20
    return 11 + day


if __name__ == '__main__':
    print(get_around(108.786, 34.335, 1000))
