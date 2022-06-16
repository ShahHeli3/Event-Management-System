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


class QuestionAnswerForum(models.Model):
    """
    model for questions and answers
    """
    user = models.ForeignKey(User, on_delete=SET(AnonymousUser.id))
    question = models.TextField()
    answer = models.TextField(null=True)


class EventCategories(models.Model):
    """
    model for event categories
    """
    event_category = models.CharField(max_length=200)

    def __str__(self):
        return self.event_category


class Events(models.Model):
    """
    model for events
    """
    event_name = models.TextField()
    event_details = models.TextField()
    event_category = models.ForeignKey(EventCategories, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_name


class EventIdeas(models.Model):
    """
    model for event ideas
    """
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
    event_idea = models.TextField()
    event_city = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)


class EventImages(models.Model):
    """
    model for event's images
    """
    event_idea_id = models.ForeignKey(EventIdeas, on_delete=models.CASCADE, related_name='image_set')
    event_image = models.ImageField(upload_to="event_images/")
    event_image_title = models.CharField(max_length=200)
    event_image_details = models.TextField()
