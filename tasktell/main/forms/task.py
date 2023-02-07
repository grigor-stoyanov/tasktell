from django import forms
from tasktell.main.models import Tasks
import re


class CreateTaskForm(forms.ModelForm):

    def save(self, commit=True):
        if commit:
            task_listid = list(dict(self.data).keys())[-1]
            task_listid = re.search(r'(\d+)$', task_listid).group()
            self.instance.task_list_id = task_listid
            self.instance.created_by = self.initial['created_by']
            self.instance.project = self.initial['project']
            self.instance.save()

    class Meta:
        fields = ('name', 'description', 'energy')
        model = Tasks




class DeleteTaskForm(forms.ModelForm):
    class Meta:
        fields = ()
        model = Tasks
