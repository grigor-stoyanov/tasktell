from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import FormMixin, BaseFormView, ModelFormMixin, ProcessFormView

from tasktell.main.forms.project import ProjectCreateForm, PublicProjectForm
from tasktell.main.forms.task import CreateTaskForm
from tasktell.main.models import Member, Project, Tasks

UserModel = get_user_model()


class ProjectCreateView(CreateView):
    form_class = ProjectCreateForm
    template_name = 'project/project-create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save()
        member = Member.objects.create(user_id=self.request.user.pk, role=Member.Roles.OWNER)
        member.projects.add(self.object)
        return super().form_valid(form)


class PublicProjectsListView(CreateView):
    template_name = 'public.html'
    form_class = PublicProjectForm
    success_url = reverse_lazy('public projects')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context

    def form_valid(self, form):
        member = Member.objects.create(user_id=self.request.user.pk, role=Member.Roles.APP)
        member.save()
        member.projects.add(Project.objects.get(pk=self.request.POST['apply-pk']))
        return redirect(reverse_lazy('public projects'))


class ProjectDetailsView(FormMixin, DetailView):
    template_name = 'project/project.html'
    model = Project
    form_class = CreateTaskForm
    context_object_name = 'project'
    def get_initial(self):
        initial = super().get_initial()
        initial['project'] = self.object
        initial['created_by'] = self.request.user

        return initial

    def get_success_url(self):
        return reverse('project details', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailsView, self).get_context_data(**kwargs)
        context['members'] = self.object.member_set.select_related()
        context['tasks'] = self.object.tasks_set.prefetch_related()
        context['form'] = CreateTaskForm(initial={'project': self.object, 'created_by': self.request.user})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(ProjectDetailsView, self).form_valid(form)
