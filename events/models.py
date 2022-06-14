from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models import SET

from accounts.models import User


class Testimonials(models.Model):
    user = models.ForeignKey(User, on_delete=SET(AnonymousUser.id), related_name='user', null=True)
    review = models.TextField()

    def __str__(self):
        return self.user.username
