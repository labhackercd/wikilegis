from django.test import TestCase
from templatetags import auth2
import models
from django.test.client import Client


class TestUserLogin(TestCase):
    def test_is_account_login_page(self):
        client = Client()
        response = client.get('/accounts/login/')
        self.failUnlessEqual(response.status_code, 200)
