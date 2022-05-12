from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse

from tasktell.common.validators import UserExistsValidator
from tasktell.main.models import Member
from tasktell.main.tasks import send_registration_email


class MemberUsernameContains(forms.Form):
    contains = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'filter by name'
            }
        )
    )


class InviteMemberForm(forms.Form):
    def save(self):
        send_registration_email.delay(self.initial["project"].name,
                                      self.initial["created_by"].username,
                                      reverse("accept invite", kwargs={"pk": self.initial["project"].pk}),
                                      self.cleaned_data["email"])

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email'
            }
        ),
        validators=(UserExistsValidator(get_user_model().objects.filter(is_staff=False).select_related()),)
    )


class ChangeRoleForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ()
