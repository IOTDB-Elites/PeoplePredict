# constant
import datetime
from peoplePredict.database.dao import Dao

INVALID = 0
CURRENT = 1
PREDICT = 2

PEOPLE_NUM_DATABASE = 'hist_loc_unum'

# env
dao = Dao()


# interface
def get_map_data(month, day, hour):
    status = check_is_valid(month, day, hour)

    if status == INVALID:
        return build_error_resp(
            'Invalid date param. Month: ' + str(month) + ' day: ' + str(day) + ' hour: ' + str(hour))

    # if status == CURRENT:
    res = []
    for row in dao.read_data_from_target_database(PEOPLE_NUM_DATABASE, {'month': month,
                                                                       'day': day,
                                                                       'hour': hour}):
        res.append({'lng': row['lng_gcj02'], 'lat': row['lat_gcj02'], 'val': row['value']})

    return {'success': True,
            'data': res}


def get_radius_data(month, day, hour, lng, lat, radius):
    status = check_is_valid(month, day, hour)

    if status == INVALID:
        return build_error_resp(
            'Invalid date param. Month: ' + str(month) + ' day: ' + str(day) + ' hour: ' + str(hour))

    total_count = 0
    min_lat, max_lat, min_lng, max_lng = get_around(lat, lng, radius)
    # if status == CURRENT:
    for row in dao.read_data_from_target_database(PEOPLE_NUM_DATABASE, {'month': month,
                                                                       'day': day,
                                                                       'hour': hour,
                                                                       'lng_gcj02': {'$gt': min_lng,
                                                                                     '$lt': max_lng},
                                                                       'lat_gcj02': {'$gt': min_lat,
                                                                                     '$lt': max_lat}}):
        total_count += row['value']

    return {'success': True,
            'data': total_count}


def get_point_data(month, day, hour, lng, lat):
    cur_date = datetime.date(2019, month, day)
    cur_date -= datetime.timedelta(days=3)
    res = []
    for i in range(7):
        num = 0
        month = cur_date.month
        day = cur_date.day
        for row in dao.read_data_from_target_database(PEOPLE_NUM_DATABASE, {'month': month,
                                                                           'day': day,
                                                                           'hour': hour,
                                                                           'lng_gcj02': round(float(lng), 3),
                                                                           'lat_gcj02': round(float(lat), 3)}):
            num += row['value']

        res.append({'month': month, 'day': day, 'val': num})
        cur_date += datetime.timedelta(days=1)

    return {'success': True,
            'data': res}


def get_top_ten_street(month, day, hour):
    status = check_is_valid(month, day, hour)

    if status == INVALID:
        return build_error_resp(
            'Invalid date param. Month: ' + str(month) + ' day: ' + str(day) + ' hour: ' + str(hour))

    position_map = {}
    for row in dao.read_data_from_target_database(PEOPLE_NUM_DATABASE, {'month': month,
                                                                       'day': day,
                                                                       'hour': hour}):
        key = row['name']
        if key in position_map:
            position_map[key] = position_map[key] + row['value']
        else:
            position_map[key] = row['value']

    res = []
    for key in position_map:
        res.append((key, position_map[key]))
    res.sort(key=lambda x: x[1])

    return {'success': True,
            'data': res[0:10]}


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


if __name__ == '__main__':
    print(get_around(108.786, 34.335, 1000))
