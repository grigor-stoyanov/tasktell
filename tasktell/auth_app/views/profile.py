from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView

from tasktell.auth_app.forms import EditProfileForm, DeleteProfileForm
from tasktell.auth_app.models import Profile
from tasktell.main.models import Member, Project

UserData = get_user_model()


class ProfileDetailsView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'auth/profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.prefetch_related().filter(member__user_id=self.request.user.pk)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        my_profile = qs.filter(pk=self.request.user.pk)
        projects = Project.objects.prefetch_related().filter(member__user_id=self.request.user.pk)
        co_members = []
        for project in projects:
            co_members.extend(list(project.member_set.all()))
        if not self.request.user.is_superuser:
            qs = (qs.filter(user__member__in=co_members) | my_profile).distinct()
        return qs


class EditProfileView(UpdateView):
    model = Profile
    template_name = 'auth/profile/profile_edit.html'
    form_class = EditProfileForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})


class DeleteProfileView(UpdateView):
    model = Profile
    template_name = 'auth/profile/profile_delete.html'
    form_class = DeleteProfileForm
    success_url = reverse_lazy('home')
