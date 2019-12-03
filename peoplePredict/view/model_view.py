from django.http import HttpResponse
from peoplePredict.model.null_model import NullModel
from peoplePredict.model.poi_model.poi_model import PoiModel
import json

models = {'null_model': NullModel(), 'poi_model': PoiModel()}


def predict(request):
    param = request.GET
    if 'name' not in param:
        res = {'success': False,
               'message': 'name parameter is not present in request'}
        return HttpResponse(json.dumps(res))

    if param['name'] not in models:
        res = {'success': False,
               'message': "we don't have model called " + param['name']}
        return HttpResponse(json.dumps(res))

    model = models[param['name']]
    res = {'success': True,
           'model': model.name,
           'result': model.predict(param)}
    return HttpResponse(json.dumps(res))

