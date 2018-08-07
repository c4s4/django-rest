# encoding: UTF-8

from api.models import Customer
from api.common import json_to_model
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.http import require_GET, require_POST
from django.contrib.admin.views.decorators import staff_member_required


@require_GET
@staff_member_required
def customer(request, id):
    """
    Method: GET
    Path: /api/customer/<id>
    Get given customer:
    - id: the customer ID
    Return: the customer as Json
    """
    return Customer.objects.get(id=id)


@require_GET
@staff_member_required
def customer_since(request, time):
    """
    Method: GET
    Path: /api/customer/since/<time>
    Get customers modified since given time:
    - time: last modification time in ISO format, such as '2018-08-07T12:13:00+02:00'
    Return: the customers as Json
    """
    return list(Customer.objects.filter(modification_time__gte=time))


@require_POST
@staff_member_required
def customer_create(request):
    """
    Method: POST
    Path: /api/customer/create
    Create a customer:
    - data: customer fields as json in request body
    Return: nothing
    """
    customer = json_to_model(request.body.decode('utf-8'), Customer)
    customer.save()
    return HttpResponse()


@require_GET
@staff_member_required
def customer_search(request):
    """
    Method: GET
    Path: /api/customer/search<id>
    Search for customers. Search parameters are passed on the URL.
    Return: the customers list
    """
    filters = dict(request.GET.items())
    return list(Customer.objects.filter(**filters))
