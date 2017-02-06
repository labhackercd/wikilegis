from accounts import models
from django.test import TestCase


class ModelsTestCase(TestCase):

    def test_create_user(self):
        user = models.User.objects.create_user('email@test.com', 'pass')
        self.assertEquals(user.is_superuser, False)

    def test_raise_miss_email_error(self):
        with self.assertRaises(ValueError):
            models.User.objects.create_user('', 'pass')

    def test_create_superuser(self):
        user = models.User.objects.create_superuser('email@test.com', 'pass')
        self.assertEquals(user.is_superuser, True)

    def test_create_superuser_raise_value_error(self):
        with self.assertRaises(ValueError):
            models.User.objects.create_superuser('email@test.com', 'pass',
                                                 is_superuser=False)
