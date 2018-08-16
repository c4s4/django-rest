# encoding: UTF-8
# pylint: disable=no-member,unused-argument

'''
Module for views.
'''

from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.admin.views.decorators import staff_member_required
from api.models import Customer
from api.common import json_to_model


@require_GET
@staff_member_required
def customer(request, customer_id):
    """
    Method: GET
    Path: /api/customer/<id>
    Get given customer:
    - id: the customer ID
    Return: the customer as Json
    """
    return Customer.objects.get(id=customer_id)


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
    json_to_model(request.body.decode('utf-8'), Customer).save()
    return HttpResponse()


@require_GET
@staff_member_required
def customer_search(request):
    """
    Method: GET
    Path: /api/customer/search<id>
    Search for customers. Search parameters are passed as URL parameters. Thus to get customers
    with named Bob, you would add parameters '?first_name=Bob'.
    Return: the customers list
    """
    filters = dict(request.GET.items())
    return Customer.objects.filter(**filters)
