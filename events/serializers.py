from rest_framework import serializers

from accounts.models import User
from .models import Testimonials, QuestionAnswerForum, EventCategories, Events
from .utils import Util


class ViewTestimonialSerializer(serializers.ModelSerializer):
    """
    serializer to view testimonials
    """

    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        try:
            return obj.user.username
        except AttributeError:
            return "AnonymousUser"

    class Meta:
        model = Testimonials
        fields = ['user', 'review']


class AddTestimonialSerializer(serializers.ModelSerializer):
    """
    serializer to add testimonials
    """

    class Meta:
        model = Testimonials
        fields = ['user', 'review']


class QuestionAnswersSerializer(serializers.ModelSerializer):
    """
    serializer to view question answers forum
    """

    user = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = QuestionAnswerForum
        fields = ['user', 'question', 'answer']

    def get_user(self, obj):
        try:
            return obj.user.username
        except AttributeError:
            return "AnonymousUser"

    def get_answer(self, obj):
        if obj.answer:
            return obj.answer
        else:
            return "This question hasn't been answered yet"


class AddQuestionSerializer(serializers.ModelSerializer):
    """
    serializer to add questions
    """

    class Meta:
        model = QuestionAnswerForum
        fields = ['user', 'question']

    def validate(self, attrs):
        """
        sends an email to all the event managers that a new question has been posted
        """
        managers = User.objects.filter(is_event_manager=True)
        managers_email = [i.email for i in managers]

        user = attrs.get('user')

        # send mail to all the event managers that a new question has been posted
        body = "Question : " + attrs.get('question') + "\nPosted by : " + user.username
        data = {
            'subject': 'New Question Posted',
            'body': body,
            'to_email': managers_email
        }
        Util.send_mail(data)
        return attrs


class AddAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionAnswerForum
        fields = '__all__'

    def validate(self, attrs):
        """
        sends an email to user whose question has been updated
        """
        user = attrs.get('user')
        answer = attrs.get('answer')
        question = attrs.get('question')

        # send mail to the user that his/her question has been answered
        body = "Question : " + question + "\nAnswer : " + answer
        data = {
            'subject': "Your question has been answered",
            'body': body,
            'to_email': [user.email]
        }
        Util.send_mail(data)
        return attrs


class GetEventCategoriesSerializer(serializers.ModelSerializer):
    """
    serializer to view event categories
    """
    class Meta:
        model = EventCategories
        fields = ['event_category']


class EventCategoriesSerializer(serializers.ModelSerializer):
    """
    serializer to add, update and delete event categories
    """
    class Meta:
        model = EventCategories
        fields = ['id', 'event_category']


class GetEventsSerializer(serializers.ModelSerializer):
    """
    serializer to view events
    """
    class Meta:
        model = Events
        fields = ['event_category', 'event_name', 'event_details']

    event_category = serializers.SerializerMethodField()

    def get_event_category(self, obj):
        return obj.event_category.event_category


class EventsSerializer(serializers.ModelSerializer):
    """
    serializer to add, update and delete events
    """
    class Meta:
        model = Events
        fields = '__all__'





