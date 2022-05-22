from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from tasktell.chat.forms import SendMessageForm
from tasktell.chat.models import Chat, Messages
from tasktell.common.helpers import get_logged_in_user_as_member_or_none
from tasktell.main.models import Project


class ChatDetailsView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/chat.html'
    model = Project
    form_class = SendMessageForm

    def get_success_url(self):
        return reverse('chat', kwargs={'pk': self.kwargs['pk'], 'id': self.kwargs['id']})

    def get_initial(self):
        initial = super().get_initial()
        initial['created_by'] = self.request.user
        initial['sent_to'] = Chat.objects.get(pk=self.kwargs['id'])
        initial['sent_from'] = Chat.objects.get(
            members_id=get_logged_in_user_as_member_or_none(self.kwargs['pk'], self.request.user.pk))
        return initial

    def get_context_data(self, **kwargs):
        context = super(ChatDetailsView, self).get_context_data(**kwargs)
        current_chat = Chat.objects.get(pk=self.kwargs['id'])
        user_member = self.object.member_set.select_related().get(projects=self.kwargs['pk'],
                                                                  user_id=self.request.user.pk)
        my_chat = Chat.objects.get(members_id=user_member.pk, project_id=self.kwargs['pk'])
        context['chat_list'] = Chat.objects.filter(project_id=self.kwargs['pk']).exclude(members_id=user_member.pk)
        context['current_chat'] = current_chat
        received_messages = Messages.objects.select_related().filter(chat_id=my_chat.pk,
                                                                     created_by=current_chat.members.user.pk)
        sent_messages = Messages.objects.select_related().filter(chat_id=current_chat.pk,
                                                                 created_by=self.request.user.pk)
        context['messages'] = received_messages | sent_messages
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = SendMessageForm(**self.get_form_kwargs())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
