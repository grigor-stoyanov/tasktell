from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

import tasktell.settings
from tasktell.auth_app.models import Profile
from tasktell.main.models import Project, Member, Tasks, TaskList


class TestTask(TestCase):
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

    def test_create_new_task_successful(self):
        new_project = Project.objects.create(name='public project', type='Public')
        new_member = Member.objects.create(user_id=self.user.pk, role='Moderator')
        new_member.projects.add(new_project)
        tasklist = TaskList.objects.create(title='nothing', project_id=new_project.pk)
        data = {'name': 'asdasd',
                'description': 'something',
                'energy': 1,
                'created_by': self.user.pk,
                'project_id': new_project.pk,
                f'add_task{tasklist.id}': f'add_task{tasklist.id}'
                }
        response = self.client.post(reverse('project details', kwargs={'pk': new_project.pk}),
                                    data=data, follow=True)
        self.assertEqual(data['name'], Tasks.objects.first().name)
        self.assertContains(response, data['name'], status_code=200)

    def test_update_new_task_successful(self):
        new_project = Project.objects.create(name='public project', type='Public')
        new_member = Member.objects.create(user_id=self.user.pk, role='Moderator')
        new_member.projects.add(new_project)
        tasklist = TaskList.objects.create(title='nothing', project_id=new_project.pk)
        task = Tasks.objects.create(name='something', description='another', energy=1, created_by=self.user,
                                    project_id=new_project.pk, task_list_id=tasklist.pk)
        CHANGED_DATA = {'name': 'asdasd',
                        'description': 'something',
                        'energy': 1,
                        'created_by': self.user,
                        'project_id': new_project.pk,
                        f'add_task{tasklist.id}': f'add_task{tasklist.id}'
                        }
        response = self.client.post(reverse('edit task', kwargs={'pk': new_project.pk, 'id': task.pk}),
                                    follow=True, data=CHANGED_DATA)
        self.assertEqual(CHANGED_DATA['name'], Tasks.objects.first().name)
        self.assertContains(response, CHANGED_DATA['name'])

    def test_delete_task_successful(self):
        new_project = Project.objects.create(name='public project', type='Public')
        new_member = Member.objects.create(user_id=self.user.pk, role='Moderator')
        new_member.projects.add(new_project)
        tasklist = TaskList.objects.create(title='nothing', project_id=new_project.pk)
        task = Tasks.objects.create(name='something', description='another', energy=1, created_by=self.user,
                                    project_id=new_project.pk, task_list_id=tasklist.pk)
        response = self.client.post(reverse('delete task', kwargs={'pk': new_project.pk, 'id': task.pk}),
                                    follow=True)
        self.assertIsNone(Tasks.objects.first())
        self.assertNotContains(response, task.name)

    def test_task_mark_as_done_successful(self):
        new_project = Project.objects.create(name='public project', type='Public')
        new_member = Member.objects.create(user_id=self.user.pk, role='Moderator')
        new_member.projects.add(new_project)
        tasklist = TaskList.objects.create(title='nothing', project_id=new_project.pk)
        task = Tasks.objects.create(name='something', description='another', energy=1, created_by=self.user,
                                    project_id=new_project.pk, task_list_id=tasklist.pk)
        response = self.client.post(reverse('complete task', kwargs={'pk': new_project.pk, 'id': task.pk}),
                                    follow=True)
        self.assertTrue(Tasks.objects.first().is_done)
        self.assertContains(response,'Undo')
        response = self.client.post(reverse('complete task', kwargs={'pk': new_project.pk, 'id': task.pk}),
                                    follow=True)
        self.assertFalse(Tasks.objects.first().is_done)
        self.assertContains(response,'Done')