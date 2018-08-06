# encoding: UTF-8

from django.core import serializers
from django.http import HttpResponse
from django.db.models.query import QuerySet


def json_middleware(get_response):
    '''
    Middleware that turn QuerySet responses into Json.
    '''

    def middleware(request):
        response = get_response(request)
        # if response is QuerySet, return Json
        if isinstance(response, QuerySet):
            json = serializers.serialize('json', response)
            response = HttpResponse(json, content_type='application/json')
        return response

    return middleware
