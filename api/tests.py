import json
from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from cheapiesgr.models import *
from .views import AUTH_TOKEN_LABEL

def decode_response(response):
    return json.loads(response.content.decode('utf-8'))

class APITestcase(TestCase):

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

    def logout(self):
        print(self.header)

        logout_response = self.client.post('/observatory/api/logout/', **self.header)
        logout_response = decode_response(logout_response)
        assert(logout_response['message'] == 'OK')
