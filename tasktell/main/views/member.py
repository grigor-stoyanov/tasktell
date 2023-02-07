from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView
from django.views.generic.edit import UpdateView

from tasktell.chat.models import Chat
from tasktell.common.decorators import require_http_methods_mod_and_owner, require_http_methods_owner
from tasktell.common.helpers import get_logged_in_user_as_member_or_none
from tasktell.main.forms.member import InviteMemberForm, ChangeRoleForm
from tasktell.main.models import Member, Project
from tasktell.main.views.project import ProjectDetailsView


@method_decorator(require_http_methods_mod_and_owner(request_method_set={'GET'}), name='dispatch')
class InviteMemberView(ProjectDetailsView):
    form_class = InviteMemberForm

    def get_success_url(self):
        return reverse('project details', kwargs={'pk': self.get_object().pk})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            response = HttpResponseRedirect(self.get_success_url())
            response.set_cookie('form_errors', form.errors)
        return response

    def form_valid(self, form):
        form.save()
        response = HttpResponseRedirect(self.get_success_url())
        response.set_cookie('form_errors', form.errors)
        return response


class MemberChangeStatusView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('project details', args=(self.kwargs['pk'],))


class AcceptInviteView(MemberChangeStatusView):
    def dispatch(self, request, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs['pk'])
        user_member = get_logged_in_user_as_member_or_none(project.pk, self.request.user.pk)
        if not user_member:
            new_member = Member(role=Member.Roles.MEMBER, user_id=request.user.pk)
            new_member.save()
            Chat.objects.create(members_id=new_member.pk, project_id=project.pk)
            new_member.projects.add(project)

        return super().dispatch(request, *args, **kwargs)


class LeaveTeamView(MemberChangeStatusView):
    def get_redirect_url(self, pk):
        return reverse('home')

    def dispatch(self, request, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs['pk'])
        member = project.member_set.select_related().get(user_id=self.request.user.pk)
        if member.role == Member.Roles.OWNER:
            project.member_set.select_related().delete()
            project.delete()
        else:
            member.delete()
        return super().dispatch(request, *args, **kwargs)


@method_decorator(require_http_methods_owner(request_method_set={'GET'}), name='dispatch')
class RemoveFromTeamView(MemberChangeStatusView):
    def dispatch(self, request, *args, **kwargs):
        member = Member.objects.get(pk=self.kwargs['id'])
        member.delete()
        return super().dispatch(request, *args, **kwargs)


@method_decorator(require_http_methods_owner(request_method_set={'GET'}), name='dispatch')
class ChangeRoleView(UpdateView):
    model = Member
    form_class = ChangeRoleForm

    def get_success_url(self):
        return reverse('project details', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        form = ChangeRoleForm(request.POST, instance=Member.objects.get(pk=self.kwargs['id']))
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if not form.instance.role == Member.Roles.OWNER:
            form.instance.role = form.data['Role']
            if form.instance.role == Member.Roles.OWNER:
                previous_owner = self.request.user.member_set.get(role=Member.Roles.OWNER)
                previous_owner.role = Member.Roles.MEMBER
                previous_owner.save()
            form.instance.save()
        return HttpResponseRedirect(self.get_success_url())
