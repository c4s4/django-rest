# encoding: UTF-8
# pylint: disable=invalid-name,missing-docstring

from django.urls import path

from . import views

urlpatterns = [
    path('customer/<int:customer_id>', views.customer, name='customer-get'),
    path('customer/create', views.customer_create, name='customers-create'),
    path('customer/search', views.customer_search, name='customers-search'),
]
