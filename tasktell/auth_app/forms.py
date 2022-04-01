from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from tasktell.auth_app.models import FIRST_NAME_MAX_LENGTH, LAST_NAME_MAX_LENGTH, USERNAME_MAX_LENGTH, GENDERS, Profile
from tasktell.common.mixins import FormBootstrapMixin


class AuthForm(AuthenticationForm, FormBootstrapMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=FIRST_NAME_MAX_LENGTH)
    last_name = forms.CharField(max_length=LAST_NAME_MAX_LENGTH)
    email = forms.EmailField()
    description = forms.CharField(widget=forms.Textarea, required=False)
    birth_date = forms.DateField()
    gender = forms.ChoiceField(choices=GENDERS)
    avatar = forms.ImageField(required=False)


class CreateUserProfileForm(FormBootstrapMixin, ProfileForm, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            avatar=self.cleaned_data['avatar'],
            description=self.cleaned_data['description'],
            gender=self.cleaned_data['gender'],
            birth_date=self.cleaned_data['birth_date'],
            user=user,
        )
        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'password1', 'password2',
            'first_name', 'last_name', 'birth_date',
            'description', 'email', 'gender', 'avatar')
