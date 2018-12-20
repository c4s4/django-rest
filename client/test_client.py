# encoding: UTF-8

from django_rest_client import DjangoRestClient


USERNAME = 'client'
PASSWORD = 'djangorest'


client = DjangoRestClient(url='http://localhost:8000', username=USERNAME, password=PASSWORD, verbose=True)
print(client.request('/api/customer/search'))
