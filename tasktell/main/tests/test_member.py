from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from tasktell.auth_app.models import Profile
from tasktell.chat.models import Chat
from tasktell.main.models import Project, Member


class TestMember(TestCase):
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
        self.second_user_data = {
            'username': 'dell2',
            'password': 'dell1234'
        }
        self.second_profile_data = {
            'first_name': 'nedelcho2',
            'last_name': 'nedelchov2',
            'birth_date': '1982-10-12',
            'email': 'nedelcho2@abv.bg',
            'gender': 'Female',
            'description': 'blablabla',
        }
        self.second_user = get_user_model().objects.create_user(**self.second_user_data)
        self.second_profile = Profile.objects.create(**self.second_profile_data, user_id=self.second_user.pk)
        self.new_project = Project.objects.create(name='public project', type='Public')
        self.new_member = Member.objects.create(user_id=self.user.pk, role='Owner')
        self.new_member.projects.add(self.new_project)
        Chat.objects.create(members_id=self.new_member.pk, project_id=self.new_project.pk)
        self.second_member = Member.objects.create(user_id=self.second_user.pk, role='Moderator')
        Chat.objects.create(members_id=self.second_member.pk, project_id=self.new_project.pk)
        self.second_member.projects.add(self.new_project)

    def test_accept_invitation_link_successful(self):
        another_project = Project.objects.create(name='public project 2', type='Public')
        self.assertNotEqual(Member.objects.last().user_id, self.user.pk)
        response = self.client.get(reverse('accept invite', kwargs={'pk': another_project.pk}), follow=True)
        self.assertEqual(Member.objects.last().user_id, self.user.pk)
        self.assertEqual(Member.objects.last().role, 'Member')
        self.assertContains(response, self.user.username)

    def test_send_invitation_link_fail_display_errors(self):
        another_project = Project.objects.create(name='public project 2', type='Public')
        another_member = Member.objects.create(user_id=self.user.pk, role='Moderator')
        another_member.projects.add(another_project)
        response = self.client.post(reverse('invite member', kwargs={'pk': another_project.pk}),
                                    data={'email': 'asd@gmail.com'}, follow=True)
        error_msg = 'Email does not match any active user.'
        self.assertContains(response, error_msg)

    def test_send_invitation_link_success(self):
        self.second_member.projects.remove()
        self.second_member.delete()
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            response = self.client.post(
                reverse('invite member', kwargs={'pk': self.new_project.pk}),
                data={'email': self.second_profile.email}, follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

    def test_leave_project_successful_as_non_owner(self):
        self.new_member.role = 'Member'
        self.new_member.save()
        self.second_member.role = 'Owner'
        self.second_member.save()
        self.assertEqual(Member.objects.first().pk, self.new_member.pk)
        response = self.client.post(reverse('leave team', kwargs={'pk': self.new_project.pk}),
                                    follow=True)
        self.assertEqual(Member.objects.first().pk, self.second_member.pk)
        self.assertNotContains(response, self.user.username)

    def test_leave_project_successful_as_owner(self):
        response = self.client.post(reverse('leave team', kwargs={'pk': self.new_project.pk}))
        self.assertIsNone(Project.objects.first())
        self.assertIsNone(Member.objects.first())
        self.assertRedirects(response, reverse('home'))

    def test_remove_member_from_project(self):
        self.assertEqual(Member.objects.last().pk, self.second_member.pk)
        response = self.client.post(
            reverse('remove from team', kwargs={'pk': self.new_project.pk, 'id': self.second_member.pk})
            , follow=True)
        self.assertEqual(Member.objects.last().pk, self.user.pk)
        self.assertNotContains(response, self.second_user.username)

    def test_change_role_to_non_owner(self):
        self.assertEqual(Member.objects.last().role, 'Moderator')
        self.client.post(
            reverse('change role', kwargs={'pk': self.new_project.pk, 'id': self.second_member.pk}),
            follow=True, data={'Role': 'Member'})
        self.assertEqual(Member.objects.last().role, 'Member')

    def test_change_role_to_owner(self):
        self.assertEqual(Member.objects.last().role, 'Moderator')
        self.assertEqual(Member.objects.first().role, 'Owner')
        self.client.post(
            reverse('change role', kwargs={'pk': self.new_project.pk, 'id': self.second_member.pk}),
            follow=True, data={'Role': 'Owner'})
        self.assertEqual(Member.objects.last().role, 'Owner')
        self.assertEqual(Member.objects.first().role, 'Member')
