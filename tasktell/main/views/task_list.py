from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView

from tasktell.main.forms.task_list import DeleteTaskListForm
from tasktell.main.models import TaskList


class TaskListDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskList
    template_name = 'project/project.html'
    form_class = DeleteTaskListForm

    def get_success_url(self):
        project = self.object.project
        return reverse_lazy('project details', kwargs={'pk': project.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['taskboards'] = TaskList.objects.all()
        context['project'] = self.object.project
        return context
