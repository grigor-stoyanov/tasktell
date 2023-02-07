from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django import forms

from tasktell.chat.models import Messages


def send_channel_message(group_name, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_message_to_frontend',
            'message': message
        }
    )


class SendMessageForm(forms.ModelForm):
    def save(self, commit=True):
        send_channel_message(f'chat_{self.initial["sent_to"].members.user.pk}', self.initial['sent_from'].pk)
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
                    'class': 'form-control',
                    'id': 'message'
                }
            )
        }
