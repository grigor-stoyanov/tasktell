from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from tasktell.auth_app.forms import AuthForm


class TestLogin(TestCase):
    def setUp(self) -> None:
        self.user_data = {
            'username': 'dell',
            'password': 'dell123'
        }
        get_user_model().objects.create_user(**self.user_data)
        self.error_message = 'Please enter a correct username and password.' \
                             ' Note that both fields may be case-sensitive. '

    def test_login_successful_and_redirect_to_home(self):
        response = self.client.post(reverse('login'), data=self.user_data)
        self.assertRedirects(response, reverse('home'))

    def test_login_unsuccessful_no_such_user_display_errors(self):
        INVALID_USER_DATA = {
            'username': 'blabla',
            'password': 'moreblabla'
        }
        response = self.client.post(reverse('login'), data=INVALID_USER_DATA)
        self.assertFormError(response, 'form', None, self.error_message)

    def test_login_unsuccessful_wrong_password_display_errors(self):
        INVALID_USER_DATA = {
            'username': 'dell',
            'password': 'moreblabla'
        }
        response = self.client.post(reverse('login'), data=INVALID_USER_DATA)
        self.assertFormError(response, 'form', None,self.error_message)
