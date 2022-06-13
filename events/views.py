from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from .models import Testimonials
from .serializers import ViewTestimonialSerializer


class ViewTestimonials(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ViewTestimonialSerializer
    queryset = Testimonials.objects.all()

    def get(self, request):
        return self.list(request)


class AddTestimonials(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = ViewTestimonialSerializer
    queryset = Testimonials.objects.all()
    # permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        user = self.request.user
        print("----------------------", user,"----",id)
        return self.create(request, id)
