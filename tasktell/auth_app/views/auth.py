from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from tasktell.auth_app.forms import CreateUserProfileForm, AuthForm


class UserLoginView(LoginView):
    template_name = 'auth/login.html'
    form_class = AuthForm
    def get_success_url(self):
        return reverse_lazy('home')


class UserProfileRegisterView(CreateView):
    template_name = 'auth/register.html'
    form_class = CreateUserProfileForm
    success_url = reverse_lazy('home')
