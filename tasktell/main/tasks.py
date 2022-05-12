import time

from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import EmailMessage


@shared_task
def send_registration_email(project, owner, url, recipient):
    email = EmailMessage(
        subject='TaskTell Project Invitation',
        body=f'You have been invited to join {project} by {owner}.\
                 To join click the link http://127.0.0.1:8000{url}',
        from_email=None,
        to=[f'{recipient}'],
        headers={'Content-Type': 'text/plain'},
    )
    email.send()
