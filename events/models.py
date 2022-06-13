from django.db import models
from django.db.models import SET

from accounts.models import User


class Testimonials(models.Model):
    user = models.ForeignKey(User, on_delete=SET('Anonymous User'))
    review = models.TextField()

    def __str__(self):
        return self.review
