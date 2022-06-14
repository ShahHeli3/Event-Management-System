from rest_framework import generics, status
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Testimonials
from .serializers import ViewTestimonialSerializer, AddTestimonialSerializer


class ViewTestimonials(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ViewTestimonialSerializer
    queryset = Testimonials.objects.all()

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
