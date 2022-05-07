from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from tasktell.auth_app.forms import CreateUserProfileForm, AuthForm, PasswordResetForm


class UserLoginView(LoginView):
    template_name = 'auth/login.html'
    form_class = AuthForm

    def get_success_url(self):
        return reverse_lazy('home')


class UserProfileRegisterView(CreateView):
    template_name = 'auth/register.html'
    form_class = CreateUserProfileForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], )
        login(self.request, user)
        return HttpResponseRedirect(reverse('home'))


class ResetPasswordView(PasswordChangeView):
    template_name = 'auth/change_password.html'
    form_class = PasswordResetForm
