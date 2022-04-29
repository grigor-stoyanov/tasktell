from django.test import TestCase, Client


class TestLogin(TestCase):
    def test_login_successful_and_redirect_to_home(self):
        
