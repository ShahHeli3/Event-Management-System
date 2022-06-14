from rest_framework import serializers

from accounts.models import User
from .models import Testimonials, QuestionAnswerForum
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

        # send mail to all the event managers
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
