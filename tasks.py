import os

from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_mail(data):
    email = EmailMessage(
        subject=data['subject'],
        body=data['body'],
        from_email=os.environ.get('EMAIL_FROM'),
        to=data['to_email']
    )
    email.send()
    return 'Email sent'
