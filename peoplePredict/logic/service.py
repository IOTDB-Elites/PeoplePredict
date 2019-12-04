# interface
def get_map_data(month, day, hour):
    pass


def get_radius_data(month, day, hour, lng, lat, radius):
    pass


def get_point_data(month, day, hour, lng, lat):
    pass


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


if __name__ == '__main__':
    print(get_around(108.913, 34.197, 10 * 1000))
