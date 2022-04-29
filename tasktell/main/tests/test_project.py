from django.test import TestCase, Client,override_settings


class ProjectCreateTest(TestCase):
    def setUp(self) -> None:
        self.test_client = Client()

    @override_settings(ALLOWED_HOSTS=['127.0.0.1'])
    def test_create_valid_project(self):
        VALID_PROJECT_DATA = {
            'name': 'asd',
            'type': 'public',
            'logo': '',
            'description': ''
        }
        response = self.test_client.post('create-project/', VALID_PROJECT_DATA)
        a = 5