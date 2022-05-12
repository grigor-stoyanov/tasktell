from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator

from tasktell.chat.models import Chat
from tasktell.common.decorators import require_http_methods_mod_and_owner
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import FormMixin

from tasktell.common.helpers import get_logged_in_user_as_member_or_none
from tasktell.main.forms.member import MemberUsernameContains, InviteMemberForm, ChangeRoleForm
from tasktell.main.forms.project import ProjectCreateForm, PublicProjectForm
from tasktell.main.forms.task import CreateTaskForm
from tasktell.main.forms.task_list import TaskListForm
from tasktell.main.models import Member, Project, TaskList

UserModel = get_user_model()


class ProjectCreateView(LoginRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    template_name = 'project/project-create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save()
        member = Member.objects.create(user_id=self.request.user.pk, role=Member.Roles.OWNER)
        Chat.objects.create(project_id=self.object.pk, members_id=member.pk)
        member.projects.add(self.object)
        return super().form_valid(form)


class PublicProjectsListView(CreateView):
    template_name = 'public.html'
    form_class = PublicProjectForm
    success_url = reverse_lazy('public projects')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(type='Public')
        return context

    def form_valid(self, form):
        member = Member.objects.create(user_id=self.request.user.pk, role=Member.Roles.APP)
        member.save()
        Chat.objects.create(project_id=self.request.POST['apply-pk'], members_id=member.pk)
        member.projects.add(Project.objects.get(pk=self.request.POST['apply-pk']))
        return redirect(reverse_lazy('public projects'))


@method_decorator(require_http_methods_mod_and_owner(request_method_set={'GET'}), name='dispatch')
class ProjectDetailsView(FormMixin, LoginRequiredMixin, DetailView):
    template_name = 'project/project.html'
    model = Project
    form_class = CreateTaskForm
    context_object_name = 'project'

    def get_initial(self):
        initial = super().get_initial()
        initial['project'] = self.get_object()
        initial['created_by'] = self.request.user

        return initial

    def get_success_url(self):
        return reverse('project details', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailsView, self).get_context_data(**kwargs)
        filter_by_name_form = MemberUsernameContains(self.request.GET)
        filter_by_name_form.is_valid()
        filter_by_name = filter_by_name_form.cleaned_data.get('contains', '')
        context['filter_by_name'] = filter_by_name_form
        members = self.object.member_set.select_related().filter(user__username__contains=filter_by_name)
        context['members'] = members
        context['form'] = CreateTaskForm(initial={'project': self.object, 'created_by': self.request.user})
        context['form2'] = TaskListForm()
        context['form3'] = InviteMemberForm()
        context['form3errors'] = self.request.COOKIES.get('form_errors', '')
        context['form4'] = ChangeRoleForm()
        context['taskboards'] = TaskList.objects.filter(project_id=self.object.pk)
        context['user_member'] = get_logged_in_user_as_member_or_none(self.get_object().pk, self.request.user.pk)
        if context['user_member']:
            context['chat'] = Chat.objects.exclude(members_id=context['user_member'].pk).first()
        return context

    def post(self, request, *args, **kwargs):
        if not request.POST.get('title', False):
            self.object = self.get_object()
            form = self.get_form()
        else:
            self.object = self.get_object()
            form = TaskListForm(**self.get_form_kwargs())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(ProjectDetailsView, self).form_valid(form)
