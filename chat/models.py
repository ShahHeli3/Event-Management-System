from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models import SET

from accounts.models import User


class Message(models.Model):
    """
    model for chat
    """
    sender_user = models.ForeignKey(User, related_name='sender', on_delete=SET(AnonymousUser.id))
    receiver_user = models.ForeignKey(User, related_name='receiver', on_delete=SET(AnonymousUser.id))
    message = models.TextField()
    room_name = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
