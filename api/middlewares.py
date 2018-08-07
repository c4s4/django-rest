# encoding: UTF-8

from .common import model_to_json, models_to_json
from django.http import HttpResponse
from django.db.models import Model


def json_middleware(get_response):
    '''
    Middleware that turn models into Json.
    '''
    def middleware(request):
        response = get_response(request)
        # if response is a model, serialize in json
        if isinstance(response, Model):
            response = HttpResponse(model_to_json(response), content_type='application/json')
        # if response is a list or tuple of models, serialize in json
        elif isinstance(response, (list, tuple)):
            response = HttpResponse(models_to_json(response), content_type='application/json')
        return response
    return middleware
