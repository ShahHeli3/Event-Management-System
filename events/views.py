from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from constants import ACCESS_DENIED, DELETE_TESTIMONIAL, DELETE_REVIEW
from .models import Testimonials, QuestionAnswerForum, EventCategories, Events, EventIdeas, EventImages, EventReviews
from .serializers import ViewTestimonialSerializer, AddTestimonialSerializer, QuestionAnswersSerializer, \
    AddQuestionSerializer, AddAnswerSerializer, EventCategoriesSerializer, EventsSerializer, GetEventsSerializer, \
    GetEventCategoriesSerializer, GetEventIdeasSerializer, EventImagesSerializer, EventIdeasSerializer, \
    EventReviewSerializer


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


class GetEventCategoriesView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    for viewing event categories
    """
    serializer_class = GetEventCategoriesSerializer
    queryset = EventCategories.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)


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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['event_category']
    search_fields = ['event_name', 'event_details']

    def get(self, request):
        return self.list(request)


class EventsViewSet(viewsets.ModelViewSet):
    """
    for creating, updating and deleting events
    """
    serializer_class = EventsSerializer
    queryset = Events.objects.all().order_by('id')
    permission_classes = [IsAdminUser]


class GetEventIdeasView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    class to view event ideas and its images
    """
    lookup_field = 'event_id'

    def get(self, request, event_id, *args, **kwargs):
        if request.GET.get('search_city') and request.GET.get('search_idea'):
            event_idea_queryset = EventIdeas.objects.filter(event_id=event_id,
                                                            event_idea__contains=request.GET.get('search_idea'),
                                                            event_city__contains=request.GET.get('search_city'))
        elif request.GET.get('search_city'):
            event_idea_queryset = EventIdeas.objects.filter(event_id=event_id,
                                                            event_city__contains=request.GET.get('search_city'))
        elif request.GET.get('search_idea'):
            event_idea_queryset = EventIdeas.objects.filter(event_id=event_id,
                                                            event_idea__contains=request.GET.get('search_idea'))
        else:
            event_idea_queryset = EventIdeas.objects.filter(event_id=event_id)
        event_idea_serializer = GetEventIdeasSerializer(event_idea_queryset, many=True)
        return Response({'data': event_idea_serializer.data}, status=status.HTTP_200_OK)


class EventIdeasViewSet(viewsets.ModelViewSet):
    """
    class to add,update and delete ideas
    """
    serializer_class = EventIdeasSerializer
    queryset = EventIdeas.objects.all().order_by('-create_date')
    permission_classes = [IsAdminUser]


class EventImagesViewSet(viewsets.ModelViewSet):
    """
    class to add,update and delete event images
    """
    serializer_class = EventImagesSerializer
    queryset = EventImages.objects.all().order_by('id')
    permission_classes = [IsAdminUser]


class EventReviewViewSet(viewsets.ModelViewSet):
    """
    class for adding, updating and deleting an event review
    """

    serializer_class = EventReviewSerializer
    queryset = EventReviews.objects.all()
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
            return Response({'msg': DELETE_REVIEW}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'msg': ACCESS_DENIED}, status=status.HTTP_400_BAD_REQUEST)
