from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from cloudinary.models import CloudinaryField

NAME_MAX_LENGTH = 30
UserModel = get_user_model()


class Project(models.Model):
    CHOICE_MAX_LENGTH = 50
    TYPE_PUBLIC = ('Public', 'Public')
    TYPE_PRIVATE = ('Private', 'Private')
    TYPE_CHOICES = (TYPE_PRIVATE, TYPE_PUBLIC)
    # logo = models.ImageField(upload_to='media/project_logos/', blank=True, null=True)
    logo = CloudinaryField('image')
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    type = models.CharField(
        choices=TYPE_CHOICES,
        max_length=CHOICE_MAX_LENGTH,
        default=TYPE_PUBLIC,
    )
    description = models.TextField(blank=True, null=True)


class TaskList(models.Model):
    title = models.CharField(max_length=NAME_MAX_LENGTH)

    @property
    def get_list_tasks(self):
        return self.tasks_set.select_related()

    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Tasks(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    date_added = models.DateField(auto_now=True)
    description = models.TextField()
    energy = models.IntegerField()
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE)


class Member(models.Model):
    CHOICE_MAX_LENGTH = 10

    class Roles(models.TextChoices):
        OWNER = 'Owner', "OWNER"
        MOD = 'Moderator', "MODERATOR"
        MEMBER = 'Member', "MEMBER"
        APP = 'Applicant', "APPLICANT"

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    role = models.CharField(choices=Roles.choices,
                            max_length=CHOICE_MAX_LENGTH,
                            )
    projects = models.ManyToManyField(Project)
