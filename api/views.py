from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from api.models import Customer
from django.core import serializers
from .common import json_to_model
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
@require_GET
def customer(request, id):
    """
    Method: GET
    Path: /api/customer/<id>
    Get given customer:
    - id: the customer ID
    Return: the customer as Json
    """
    return Customer.objects.get(id=id)


@staff_member_required
@require_GET
def customer_since(request, time):
    """
    Method: GET
    Path: /api/customer/since/<time>
    Get customers modified since given time:
    - time: last modification time in ISO format, such as '2018-08-07T12:13:00+02:00'
    Return: the customers as Json
    """
    return list(Customer.objects.filter(modification_time__gte=time))


@staff_member_required
@require_POST
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
