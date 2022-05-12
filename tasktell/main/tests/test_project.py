from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasktell.auth_app.models import Profile
from tasktell.main.forms.project import ProjectCreateForm
from tasktell.main.models import Project, Member


class ProjectTest(TestCase):
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

    def test_create_valid_project_expect_to_create_and_redirect_to_home(self):
        VALID_PROJECT_DATA = {
            'name': 'asd',
            'type': 'Public',
            'logo': '',
            'description': ''
        }
        form = ProjectCreateForm(VALID_PROJECT_DATA)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('create project'), data=VALID_PROJECT_DATA)
        project = Project.objects.first()
        self.assertIsNotNone(project)
        self.assertEqual(VALID_PROJECT_DATA['name'], project.name)
        self.assertEqual(VALID_PROJECT_DATA['type'], project.type)
        expected_url = reverse('home')
        self.assertRedirects(response, expected_url)

    def test_display_only_public_projects(self):
        public_project = Project.objects.create(name='public project', type='Public')
        private_project = Project.objects.create(name='private project', type='Private')
        response = self.client.get(reverse('public projects'))
        self.assertContains(response, public_project.name)
        self.assertNotContains(response, private_project.name)

    def test_apply_to_public_project_success(self):
        project = Project.objects.create(name='public project', type='Public')
        self.client.post(reverse('public projects'), data={'apply-pk': project.pk})
        self.assertEqual(self.user.pk, Member.objects.first().user_id)

    def test_project_applicant_or_none_can_only_get_project_overview(self):
        new_project = Project.objects.create(name='public project', type='Public')
        response = self.client.get(reverse('project details', kwargs={'pk': new_project.pk}))
        self.assertContains(response, 'Project Overview')
        self.assertNotContains(response, 'Project Members')
        self.assertNotContains(response, 'Project Tasks')
        new_member = Member.objects.create(user_id=self.user.pk, role='Applicant')
        new_member.projects.add(new_project)
        response = self.client.get(reverse('project details', kwargs={'pk': new_project.pk}))
        self.assertContains(response, 'Project Overview')
        self.assertNotContains(response, 'Project Members')
        self.assertNotContains(response, 'Project Tasks')
