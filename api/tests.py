# encoding: UTF-8

import json
from api.models import Customer
from django.test import TestCase, Client


class CustomerTestCase(TestCase):

    def setUp(self):
        Customer.objects.create(id=1, email='bob@example.com', first_name='Robert', last_name='Jenning', birth_date='1966-07-14')
        Customer.objects.create(id=2, email='fer@example.com', first_name='Ferdinand', last_name='Durand', birth_date='1987-08-24')

    def test_customer(self):
        client = Client()
        response = client.get('/api/customer/1')
        self.assertEqual(response.status_code, 200)
        customer = json.loads(response.content)
        expected = {
            'id': 1,
            'email': 'bob@example.com',
            'first_name': 'Robert',
            'last_name': 'Jenning',
            'birth_date': '1966-07-14',
        }
        self.assertDictEqual(customer, expected)

    def test_customer_since(self):
        client = Client()
        response = client.get('/api/customer/since/2000-01-01T00:00:00+02:00')
        self.assertEqual(response.status_code, 200)
        customers = sorted(json.loads(response.content), key=lambda c: c['id'])
        self.assertEqual(len(customers), 2)
        expected = {
            'id': 1,
            'email': 'bob@example.com',
            'first_name': 'Robert',
            'last_name': 'Jenning',
            'birth_date': '1966-07-14',
        }
        self.assertDictEqual(customers[0], expected)
    
    def test_customer_create(self):
        client = Client()
        data = {
            'email': 'rob@example.com',
            'first_name': 'Robert',
            'last_name': 'Stewart',
            'birth_date': '1976-03-04',
        }
        response = client.post('/api/customer/create', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
