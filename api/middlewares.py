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

def pagination_middleware(get_response):
    '''
    Middleware to manage pagination.
    '''
    def middleware(request):
        range = None
        if 'Range' in request.META:
            range = request.META['Range']
        response = get_response(request)
        # if pagination parameter was set, paginate response
        if range:
            if not isinstance(response, QuerySet):
                return HttpResponse(content='May only paginate QuerySet response', status=400)
            if request.method != 'GET':
                return HttpResponse(content='May only paginate GET response', status=400)
            try:
                start, end = range.split('-')
                start = int(start)
                end = int(end)
                size = response.count()
                result = response[start:end]
            except:
                return HttpResponse(content='Invalid range "%s"' % range, status=400)
            response = HttpResponse(queryset_to_json(result), status=206,
                                    content_type='application/json')
            response['Content-Range'] = range + '/%d' % size
        return response
    return middleware
