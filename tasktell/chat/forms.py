from django import forms

from tasktell.chat.models import Messages


class SendMessageForm(forms.ModelForm):
    def save(self, commit=True):
        if commit:
            self.instance.created_by_id = self.initial['created_by'].pk
            self.instance.chat_id = self.initial['sent_to'].pk
            self.instance.save()

    class Meta:
        model = Messages
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'placeholder': 'Type your message here.',
                    'class': 'form-control'
                }
            )
        }
