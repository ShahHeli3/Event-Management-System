from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models import SET

from accounts.models import User


class Testimonials(models.Model):
    """
    model for testimonials
    """
    user = models.ForeignKey(User, on_delete=SET(AnonymousUser.id), related_name='user', null=True)
    review = models.TextField()
    post_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review


# class QnAForum(models.Model):
#     """
#     model for questions and answers
#     """
#     user = models.ForeignKey(User, on_delete=SET(AnonymousUser.id), related_name='user', null=True)
#     question = models.TextField()
#     answer = models.TextField(required=False)



