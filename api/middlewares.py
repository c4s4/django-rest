# encoding: UTF-8

'''
Module for middlewares.
'''

from django.http import HttpResponse
from django.db.models import Model
from django.db.models.query import QuerySet
from .common import model_to_json, queryset_to_json


def json_middleware(get_response):
    '''
    Middleware that turn models into Json.
    '''
    def middleware(request):
        response = get_response(request)
        # if response is a model, serialize in json
        if isinstance(response, Model):
            response = HttpResponse(model_to_json(response), content_type='application/json')
        # if response is a QuerySet, serialize in json list
        elif isinstance(response, QuerySet):
            response = HttpResponse(queryset_to_json(response), content_type='application/json')
        return response
    return middleware
