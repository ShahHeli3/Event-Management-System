from rest_framework import generics, status
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Testimonials
from .serializers import ViewTestimonialSerializer, AddTestimonialSerializer


class ViewTestimonials(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ViewTestimonialSerializer
    queryset = Testimonials.objects.all().order_by('-post_date_time')

    def get(self, request):
        return self.list(request)


class AddTestimonials(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = AddTestimonialSerializer
    queryset = Testimonials.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
