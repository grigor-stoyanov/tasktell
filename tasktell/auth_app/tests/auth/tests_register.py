from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasktell.auth_app.forms import CreateUserProfileForm
from tasktell.auth_app.models import Profile


class TestRegisterUser(TestCase):
    def test_user_register_successfull_and_redirect_to_home(self):
        VALID_PROFILE_DATA = {
            'username': 'someone',
            'password1': '123',
            'password2': '123',
            'first_name': 'someone',
            'last_name': 'else',
            'birth_date': '1982-12-02',
            'email': 'someone.else@abv.bg',
            'description': '',
            'gender': 'Male',
            'avatar': ''
        }
        form = CreateUserProfileForm(VALID_PROFILE_DATA)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('register'), data=VALID_PROFILE_DATA)
        profile = Profile.objects.first()
        user = get_user_model().objects.first()
        self.assertEqual(user.username, VALID_PROFILE_DATA['username'])
        self.assertEqual(profile.email, VALID_PROFILE_DATA['email'])
        expected_url = reverse('home')
        self.assertRedirects(response, expected_url)

    def test_register_invalid_data_expect_to_show_form_errors(self):
        INVALID_PROFILE_DATA = {
            'username': 'someone',
            'password1': '123',
            'password2': '1234',
            'first_name': 'someone3',
            'last_name': 'else4',
            'birth_date': '1913-12-02',
            'email': 'someone.elseabv.bg',
            'description': '',
            'gender': 'Male6',
            'avatar': ''
        }
        form = CreateUserProfileForm(INVALID_PROFILE_DATA)
        self.assertFalse(form.is_valid())
        response = self.client.post(reverse('register'), data=INVALID_PROFILE_DATA, follow=True)
        self.assertIsNone(Profile.objects.first())
        self.assertIsNone(get_user_model().objects.first())
        self.assertFormError(response, 'form', 'last_name', form.errors['last_name'])
        self.assertFormError(response, 'form', 'first_name', form.errors['first_name'])
        self.assertFormError(response, 'form', 'password2', form.errors['password2'])
        self.assertFormError(response, 'form', 'birth_date', form.errors['birth_date'])
        self.assertFormError(response, 'form', 'gender', form.errors['gender'])
        self.assertFormError(response, 'form', 'email', form.errors['email'])



