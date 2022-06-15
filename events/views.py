from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework import mixins, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from constants import ACCESS_DENIED, DELETE_TESTIMONIAL
from .models import Testimonials, QuestionAnswerForum, EventCategories, Events
from .serializers import ViewTestimonialSerializer, AddTestimonialSerializer, QuestionAnswersSerializer, \
    AddQuestionSerializer, AddAnswerSerializer, EventCategoriesSerializer, EventsSerializer, GetEventsSerializer


class ViewTestimonials(generics.GenericAPIView, mixins.ListModelMixin):
    """
    class for viewing all the testimonials
    """
    serializer_class = ViewTestimonialSerializer
    queryset = Testimonials.objects.all().order_by('-post_date_time')

    def get(self, request):
        return self.list(request)


class TestimonialsViewSet(viewsets.ModelViewSet):
    """
    class for adding, updating and deleting a testimonial
    """

    serializer_class = AddTestimonialSerializer
    queryset = Testimonials.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.user:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({'msg': ACCESS_DENIED}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.user:
            self.perform_destroy(instance)
            return Response({'msg': DELETE_TESTIMONIAL}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'msg': ACCESS_DENIED}, status=status.HTTP_400_BAD_REQUEST)


class QuestionAnswersView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    class to view question and answers
    """

    serializer_class = QuestionAnswersSerializer
    queryset = QuestionAnswerForum.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)


class AddQuestionView(generics.GenericAPIView, mixins.CreateModelMixin):
    """
    class for adding a question
    """

    serializer_class = AddQuestionSerializer
    queryset = QuestionAnswerForum.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AddAnswerView(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """
    class for adding an answer to a posted question and deleting a question
    """

    serializer_class = AddAnswerSerializer
    queryset = QuestionAnswerForum.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'

    def put(self, request, id=None):
        instance = self.get_object()

        request.data['user'] = request.user.id
        request.data['question'] = instance.question
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


class EventCategoriesViewSet(viewsets.ModelViewSet):
    """
    for creating, updating and deleting event categories
    """
    serializer_class = EventCategoriesSerializer
    queryset = EventCategories.objects.all().order_by('id')
    permission_classes = [IsAdminUser]


class GetEventsView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    for viewing events
    """
    serializer_class = GetEventsSerializer
    queryset = Events.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['event_category']
    search_fields = ['event_category', 'event_name', 'event_details']

    def get(self, request):
        return self.list(request)


class EventsViewSet(viewsets.ModelViewSet):
    """
    for creating, updating and deleting events
    """
    serializer_class = EventsSerializer
    queryset = Events.objects.all().order_by('id')
    permission_classes = [IsAdminUser]
