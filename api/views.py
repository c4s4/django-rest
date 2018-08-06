from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from api.models import Customer
from django.core import serializers


@require_GET
def customer(request, id):
    return Customer.objects.filter(id=id)


@require_GET
def customer_since(request, time):
    return Customer.objects.filter(modification_time__gte=time)


@require_POST
def customer_create(request):
    fields = request.body.decode('utf-8')
    json = '[{"model": "api.models.Customer", "fields": %s}]' % fields
    # DEBUG
    print(">>>>>>>>", json)
    customers = serializers.deserialize('json', json)
    for customer in customers:
        customer.save()
