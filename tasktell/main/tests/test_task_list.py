from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

import tasktell.settings
from tasktell.auth_app.models import Profile
from tasktell.main.models import Project, Member, TaskList, Tasks


class TaskListTest(TestCase):
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

    def test_create_new_tasklist_successful_and_in_context(self):
        new_project = Project.objects.create(name='public project', type='Public')
        new_member = Member.objects.create(user_id=self.user.pk, role='Moderator')
        new_member.projects.add(new_project)
        data = {'title': 'asdasd'}
        response = self.client.post(reverse('project details', kwargs={'pk': new_project.pk}),
                                    data=data, follow=True)
        self.assertEqual(data['title'], TaskList.objects.first().title)
        self.assertContains(response, data['title'], status_code=200)

    def test_delete_tasklist_also_deletes_tasks(self):
        new_project = Project.objects.create(name='public project', type='Public')
        new_member = Member.objects.create(user_id=self.user.pk, role='Moderator')
        new_member.projects.add(new_project)
        tasklist = TaskList.objects.create(title='asdasd', project_id=new_project.pk)
        Tasks.objects.create(name='asd', description='sad', energy='1', project_id=new_project.pk,
                             task_list_id=tasklist.pk, created_by_id=self.user.pk)
        response = self.client.post(reverse('delete taskboard', kwargs={'pk': new_project.pk}), follow=True)
        self.assertNotContains(response, tasklist.title)
        self.assertIsNone(TaskList.objects.first())
        self.assertIsNone(Tasks.objects.first())

    def test_only_mod_and_owner_can_create_task_list(self):
        new_project = Project.objects.create(name='public project', type='Public')
        data = {'title': 'asdasd'}
        response = self.client.post(reverse('project details', kwargs={'pk': new_project.pk}),
                                    data=data, follow=True)
        self.assertEqual(response.status_code, 405)
        new_member = Member.objects.create(user_id=self.user.pk, role='Member')
        new_member.projects.add(new_project)

        response = self.client.post(reverse('project details', kwargs={'pk': new_project.pk}),
                                    data=data, follow=True)
        self.assertEqual(response.status_code, 405)
        new_member.role = 'Applicant'
        new_member.save()
        response = self.client.post(reverse('project details', kwargs={'pk': new_project.pk}),
                                    data=data, follow=True)
        self.assertEqual(response.status_code, 405)
