from django import forms
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse

from tasktell.common.validators import UserExistsValidator
from tasktell.main.models import Member


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
        send_mail(
            'TaskTell Project Invitation',
            f'You have been invited to join {self.initial["project"].name} by {self.initial["created_by"].username}.\
             To join click the link http://127.0.0.1:8000{reverse("accept invite", kwargs={"pk": self.initial["project"].pk})}',
            None,
            [f'{self.cleaned_data["email"]}'],
        )

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
