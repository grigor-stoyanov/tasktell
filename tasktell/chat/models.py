from django.contrib.auth import get_user_model
from django.db import models

from tasktell.main.models import Project, Member

UserModel = get_user_model()


class Chat(models.Model):
    members = models.ForeignKey(Member, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Messages(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
