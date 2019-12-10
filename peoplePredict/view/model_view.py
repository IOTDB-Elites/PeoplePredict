from django.http import HttpResponse
import json

from peoplePredict.logic import service

GET_MAP_DATA_PARAMS = ['month', 'day', 'hour']
GET_RADIUS_DATA_PARAMS = ['month', 'day', 'hour', 'lng', 'lat', 'radius']
GET_POINT_DATA_PARAMS = ['month', 'day', 'hour', 'lng', 'lat']
GET_TOP_TEN_STREET = ['month', 'day', 'hour']


def predict(request):
    param = request.GET
    if 'name' not in param:
        res = {'success': False,
               'message': 'name parameter is not present in request'}
        return HttpResponse(json.dumps(res))

    return HttpResponse(json.dumps({}))


def get_map_data(request):
    # check params
    error_res = check_param(request, GET_MAP_DATA_PARAMS)
    if error_res is not None:
        return warp_to_response(error_res)

    param = request.GET
    return warp_to_response(service.get_map_data(int(param['month']), int(param['day']), int(param['hour'])))


def get_radius_data(request):
    # check params
    error_res = check_param(request, GET_RADIUS_DATA_PARAMS)
    if error_res is not None:
        return warp_to_response(error_res)

    param = request.GET
    return warp_to_response(service.get_radius_data(int(param['month']), int(param['day']), int(param['hour']),
                                                    float(param['lng']), float(param['lat']), float(param['radius'])))


def get_point_data(request):
    # check params
    error_res = check_param(request, GET_POINT_DATA_PARAMS)
    if error_res is not None:
        return warp_to_response(error_res)

    param = request.GET
    return warp_to_response(service.get_point_data(int(param['month']), int(param['day']), int(param['hour']),
                                                   float(param['lng']), float(param['lat'])))


def get_top_ten_street(request):
    # check params
    error_res = check_param(request, GET_TOP_TEN_STREET)
    if error_res is not None:
        return warp_to_response(error_res)

    param = request.GET
    return warp_to_response(service.get_top_ten_street(int(param['month']), int(param['day']), int(param['hour'])))


def check_param(request, params):
    for param in params:
        if param not in request.GET:
            return {'success': False,
                    'message': param + ' parameter is not present in request'}

    return None


def warp_to_response(res):
    return HttpResponse(json.dumps(res))
