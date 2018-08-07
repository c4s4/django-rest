# encoding: UTF-8

import json
from api.models import Customer
from django.test import TestCase, Client
from django.contrib.auth.models import User


class CustomerTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username='test', password='test', email='test@example.com',  is_staff=True)
        self.client = Client()
        self.client.login(username='test', password='test')
        Customer.objects.create(id=1, email='bob@example.com', first_name='Robert', last_name='Jenning', birth_date='1966-07-14')
        Customer.objects.create(id=2, email='fer@example.com', first_name='Ferdinand', last_name='Durand', birth_date='1987-08-24')
    
    def test_customer(self):
        response = self.client.get('/api/customer/1')
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
    
    def test_customer_create(self):
        data = {
            'email': 'rob@example.com',
            'first_name': 'Robert',
            'last_name': 'Stewart',
            'birth_date': '1976-03-04',
        }
        response = self.client.post('/api/customer/create', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_customer_search(self):
        response = self.client.get('/api/customer/search?first_name=Robert')
        self.assertEqual(response.status_code, 200)
        customers = json.loads(response.content)
        self.assertEqual(len(customers), 1)
        customer = customers[0]
        expected = {
            'id': 1,
            'email': 'bob@example.com',
            'first_name': 'Robert',
            'last_name': 'Jenning',
            'birth_date': '1966-07-14',
        }
        self.assertDictEqual(customer, expected)

    def test_customer_search_two_filters(self):
        response = self.client.get('/api/customer/search?first_name=Robert&id=1')
        self.assertEqual(response.status_code, 200)
        customers = json.loads(response.content)
        self.assertEqual(len(customers), 1)
        customer = customers[0]
        expected = {
            'id': 1,
            'email': 'bob@example.com',
            'first_name': 'Robert',
            'last_name': 'Jenning',
            'birth_date': '1966-07-14',
        }
        self.assertDictEqual(customer, expected)

    def test_customer_search_endswith(self):
        response = self.client.get('/api/customer/search?email__endswith=example.com')
        self.assertEqual(response.status_code, 200)
        customers = json.loads(response.content)
        self.assertEqual(len(customers), 2)
        customer = customers[0]
        expected = {
            'id': 1,
            'email': 'bob@example.com',
            'first_name': 'Robert',
            'last_name': 'Jenning',
            'birth_date': '1966-07-14',
        }
        self.assertDictEqual(customer, expected)

    def test_customer_search_since(self):
        params = {'modification_time__gte': '2000-01-01T00:00:00+02:00'}
        response = self.client.get('/api/customer/search', data=params)
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
    
    def test_customer_search_all(self):
        response = self.client.get('/api/customer/search')
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
    