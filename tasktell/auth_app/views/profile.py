from django.contrib.auth import get_user_model
from django.views.generic import DetailView, UpdateView

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


class ProfileEditView(UpdateView):
    model = Profile
