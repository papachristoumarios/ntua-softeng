from django.http import QueryDict
import urllib
import json
import copy
from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from cheapiesgr.models import *
from .views import AUTH_TOKEN_LABEL

def decode_response(response):
    return json.loads(response.content.decode('utf-8'))

def urldump(data):
    return urllib.parse.urlencode(data)

class APITestcase(TestCase):
    #me poion tropo ginontai ta test????
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        usr = User.objects.create_user(username='test',
        email='johndoe@example.com',
        password='test',
        first_name='John',
        last_name='Doe')
        usr.save()
        volunteer = Volunteer(user=usr, confirmed_email=True)
        volunteer.save()
        login_response = self.client.post('/observatory/api/login/',
        {'username' : 'test',
        'password' : 'test'},
        format='json')
        login_response = decode_response(login_response)
        assert('token' in login_response)
        self.token = login_response['token']
        self.header = { AUTH_TOKEN_LABEL : self.token }
        self.client.credentials(HTTP_X_OBSERVATORY_AUTH=self.token)
        self.product = {
            'name' : 'foo',
            'description' : 'foo',
            'category' : 'laptop',
            'tags' : ['a', 'b'],
            'withdrawn' : False
        }
        self.products = [self.product]
        response = self.client.post('/observatory/api/products/', urldump(self.product), content_type='application/x-www-form-urlencoded')
        response = decode_response(response)
        print(response)
        self.idd = response['id']
        response = self.client.get('/observatory/api/products/{}'.format(self.idd),format = 'json')
        response = decode_response(response)
        assert(response['name'] == self.product['name'])
        assert(response['description'] == self.product['description'])
        assert(response['category'] == self.product['category'])
        assert(self.product['tags'] == response['tags'])
        assert(response['withdrawn'] == self.product['withdrawn'])
        assert(response['name'] == self.product['name'])


    def test_get_products(self):
        response = self.client.get('/observatory/api/products/',format = 'json')
        response = decode_response(response)
        assert(response['count'] == 20)
        assert(response['products'][0]['name'] == self.product['name'])

        assert(response['start'] == 0)
        assert(response['total'] == 1)

    def test_put_products(self):

        newproduct = {
            'name' : 'foo1',
            'description' : 'foo1',
            'category' : 'laptop1',
            'tags' : ['a1', 'b1'],
            'withdrawn' : False
        }
        response = self.client.put('/observatory/api/products/{}'.format(self.idd), urldump(newproduct), content_type='application/x-www-form-urlencoded')
        response = self.client.get('/observatory/api/products/{}'.format(self.idd), format = 'json')
        response = decode_response(response)
        assert(response['name'] == newproduct['name'])
        assert(response['description'] == newproduct['description'])
        assert(response['category'] == newproduct['category'])
        assert(response['tags'] == newproduct['tags'])
        assert(response['withdrawn'] == newproduct['withdrawn'])

        response = self.client.put('/observatory/api/products/{}'.format(self.idd), urldump(self.product), content_type='application/x-www-form-urlencoded')
        
    def test_patch_product(self):
        response = self.client.patch('/observatory/api/products/{}'.format(self.idd),urldump({'name':'foo2','category' : 'laptop2'}), content_type='application/x-www-form-urlencoded')
        response = self.client.get('/observatory/api/products/{}'.format(self.idd), format = 'json')
        response = decode_response(response)
        assert(response['name'] == 'foo2')
        assert(response['description'] == 'laptop2')
        response = self.client.put('/observatory/api/products/{}'.format(self.idd), urldump(self.product), content_type='application/x-www-form-urlencoded')


    def test_delete_product(self):
        response = self.client.delete('/observatory/api/products/{}'.format(self.idd))
        response = decode_response(response)
        assert(response['withdrawn'] == True)
