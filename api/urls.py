from django.urls import path

from . import views

urlpatterns = [
    path('customer/<int:id>', views.customer, name='customer'),
    path('customer/create', views.customer_create, name='customers-create'),
    path('customer/search', views.customer_search, name='customers-search'),
]
