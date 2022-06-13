from rest_framework import serializers

from accounts.models import User
from .models import Testimonials


class ViewTestimonialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Testimonials
        fields = ['user', 'review']


class AddTestimonialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Testimonials
        fields = ['review']
