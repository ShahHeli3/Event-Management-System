from rest_framework import serializers

from accounts.models import User
from .models import Testimonials


class ViewTestimonialSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Testimonials
        fields = ['user', 'review']
