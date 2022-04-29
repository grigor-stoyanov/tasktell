from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from tasktell.auth_app.models import Profile
from tasktell.main.models import Project, Member


class TestProfile(TestCase):
    def setUp(self) -> None:
        self.user_data = {
            'username': 'dell',
            'password': 'dell123'
        }
        self.profile_data = {
            'first_name': 'nedelcho',
            'last_name': 'nedelchov',
            'birth_date': '1982-10-10',
            'email': 'nedelcho@abv.bg',
            'gender': 'Male',
            'description': 'blabla',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.profile = Profile.objects.create(**self.profile_data, user_id=self.user.pk)
        self.client.login(**self.user_data)

    def test_profile_displays_associated_projects(self):
        new_project = Project.objects.create(name='project1', type='Public', )
        new_member = Member.objects.create(user_id=self.user.pk, role='Member')
        new_member.projects.add(new_project)
        response = self.client.get(reverse('profile', kwargs={'pk': self.user.pk}))
        self.assertContains(response, new_project.name)

    def test_edit_profile_success_saves_change_and_redirects_to_profile(self):
        CHANGED_DATA = {
            'first_name': self.profile.first_name,
            'last_name': self.profile.last_name,
            'birth_date': self.profile.birth_date,
            'description': self.profile.description,
            'gender': 'Female',
        }
        response = self.client.post(reverse('edit profile', kwargs={'pk': self.user.pk}), data=CHANGED_DATA)
        self.assertEqual(CHANGED_DATA['gender'], Profile.objects.first().gender)
        self.assertRedirects(response, reverse('profile', kwargs={'pk': self.user.pk}))

    def test_edit_profile_fail_remains_the_same_and_refresh_page(self):
        CHANGED_DATA = {
            'first_name': self.profile.first_name,
            'last_name': self.profile.last_name,
            'birth_date': self.profile.birth_date,
            'description': self.profile.description,
            'gender': 'non-binary'
        }
        response = self.client.post(reverse('edit profile', kwargs={'pk': self.user.pk}), data=CHANGED_DATA)
        self.assertNotEqual(CHANGED_DATA['gender'], Profile.objects.first().gender)
        self.assertNotContains(response, CHANGED_DATA['gender'])

    def test_delete_profile_deletes_associated_models(self):
        new_project = Project.objects.create(name='project1', type='Public', )
        new_member = Member.objects.create(user_id=self.user.pk, role='Owner')
        new_member.projects.add(new_project)
        second_user_data = {
            'username': 'dell2',
            'password': 'dell1234'
        }
        second_profile_data = {
            'first_name': 'nedelcho2',
            'last_name': 'nedelchov2',
            'birth_date': '1982-10-11',
            'email': 'nedelcho2@abv.bg',
            'gender': 'Female',
            'description': 'blablabla',
        }
        second_user = get_user_model().objects.create_user(**second_user_data)
        second_profile = Profile.objects.create(**second_profile_data, user_id=second_user.pk)
        second_member = Member.objects.create(user_id=second_user.pk, role='Owner')
        second_member.projects.add(new_project)

        response = self.client.post(reverse('delete profile', kwargs={'pk': self.user.pk}))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(second_user_data['username'], get_user_model().objects.first().username)
        self.assertEqual(second_profile.pk, Profile.objects.first().pk)
        self.assertIsNone(Project.objects.first())
        self.assertIsNone(Member.objects.first())
