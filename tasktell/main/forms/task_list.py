from django import forms

from tasktell.main.models import TaskList


class TaskListForm(forms.ModelForm):
    def save(self, commit=True):
        if commit:
            self.instance.project_id = self.initial['project'].pk
            self.instance.save()

    class Meta:
        model = TaskList
        fields = ('title',)


class DeleteTaskListForm(forms.ModelForm):
    def save(self, commit=True):
        if commit:
            self.instance.delete()
    class Meta:
        model = TaskList
        fields = ()
