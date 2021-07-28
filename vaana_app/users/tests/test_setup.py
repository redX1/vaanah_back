from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

        self.user_data={
            "username": "fatmalo",
            "email": "fatma.lo@terinnova.com",
            "password": "passer123",
            "gender":"F",
            "account_type":"CUSTOMER",
            "address": {
                "state":"test",
                "zipcode":"test",
                "country":"test",
                "street":"test" 
            }
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()

