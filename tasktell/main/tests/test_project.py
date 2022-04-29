from django.test import TestCase, Client
from django.urls import reverse

from tasktell.main.forms.project import ProjectCreateForm
from tasktell.main.models import Project


class ProjectCreateTest(TestCase):
    def setUp(self) -> None:
        self.test_client = Client()

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


