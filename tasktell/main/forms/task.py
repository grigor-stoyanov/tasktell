from django import forms
from tasktell.main.models import Tasks


class CreateTaskForm(forms.ModelForm):

    def save(self, commit=True):
        if commit:
            self.instance.created_by = self.initial['created_by']
            self.instance.project = self.initial['project']
            self.instance.save()

    class Meta:
        fields = ('name', 'description', 'energy')
        model = Tasks
