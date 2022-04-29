import os

from cloudinary.forms import CloudinaryFileField
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django import forms
from django.core.validators import MinLengthValidator

from tasktell.auth_app.models import FIRST_NAME_MAX_LENGTH, LAST_NAME_MAX_LENGTH, USERNAME_MAX_LENGTH, GENDERS, Profile, \
    TasktellUser, FIRST_NAME_MIN_LENGTH, LAST_NAME_MIN_LENGTH, AVATAR_MAX_SIZE, MIN_DATE
from tasktell.common.mixins import FormBootstrapMixin
from tasktell.common.validators import only_letters_validator, FileMaxSizeValidator, MinDateValidator

UserData = get_user_model()


class PasswordResetForm(PasswordChangeForm, FormBootstrapMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()


class AuthForm(AuthenticationForm, FormBootstrapMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=FIRST_NAME_MAX_LENGTH, validators=(
        only_letters_validator, MinLengthValidator(FIRST_NAME_MIN_LENGTH)))
    last_name = forms.CharField(max_length=LAST_NAME_MAX_LENGTH,
                                validators=(only_letters_validator, MinLengthValidator(LAST_NAME_MIN_LENGTH)))
    email = forms.EmailField()
    description = forms.CharField(widget=forms.Textarea, required=False)
    birth_date = forms.DateField(validators=(MinDateValidator(MIN_DATE),))
    gender = forms.ChoiceField(choices=GENDERS)
    if os.getenv('APP_ENVIRONMENT') == 'LOCAL':
        avatar = forms.ImageField(required=False, validators=(FileMaxSizeValidator(AVATAR_MAX_SIZE),))
    else:
        avatar = CloudinaryFileField()


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


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


class DeleteProfileForm(forms.ModelForm):
    def save(self, commit=True):
        # TODO add logic for deletion of user/profile related models
        TasktellUser.objects.get(pk=self.instance.pk).delete()
        self.instance.delete()
        return self.instance

    class Meta:
        model = Profile
        exclude = ('first_name', 'last_name', 'birth_date',
                   'description', 'email', 'gender', 'avatar', 'user')
