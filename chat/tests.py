from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.contrib.auth.models import User

class UserTestCase(TestCase):
    def test_user(self):
        username = 'tapan'
        password = 'Asd123!@#'
        u = User(username=username)
        u.set_password(password)
        u.save()
        self.assertEqual(u.username, username)
        self.assertTrue(u.check_password(password))