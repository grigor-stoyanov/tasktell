from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView

from tasktell.auth_app.forms import EditProfileForm, DeleteProfileForm
from tasktell.auth_app.models import Profile

UserData = get_user_model()


class ProfileDetailsView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'auth/profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({

        })
        return context


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
