from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DeleteView, RedirectView

from tasktell.common.decorators import require_http_methods_mod_and_owner
from tasktell.main.forms.task import DeleteTaskForm, CreateTaskForm
from tasktell.main.models import Project, Tasks, TaskList

decorators = [require_http_methods_mod_and_owner(request_method_set={'GET'})]


@method_decorator(decorators, name='dispatch')
class TaskEditView(LoginRequiredMixin, UpdateView):
    template_name = 'project/project.html'
    form_class = CreateTaskForm
    model = Tasks
    pk_url_kwarg = 'id'


    def get_initial(self):
        initial = super().get_initial()
        initial['created_by'] = self.request.user
        initial['project'] = self.object.project
        return initial

    def get_success_url(self):
        return reverse('project details', kwargs={'pk': self.get_object().project_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['taskboards'] = TaskList.objects.all()
        context['project'] = self.object.project
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(decorators, name='dispatch')
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'project/project.html'
    form_class = DeleteTaskForm
    model = Tasks
    pk_url_kwarg = 'id'

    def get_success_url(self):
        project = self.object.project
        return reverse_lazy('project details', kwargs={'pk': project.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['taskboards'] = TaskList.objects.all()
        context['project'] = self.object.project
        return context


class TaskCompleteView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('project details', args=(self.kwargs['pk'],))

    def dispatch(self, request, *args, **kwargs):
        task = Tasks.objects.get(pk=self.kwargs['id'])
        if not task.is_done:
            task.is_done = True
        else:
            task.is_done = False
        task.created_by_id = self.request.user.pk
        task.save()
        return super().dispatch(request, *args, **kwargs)
