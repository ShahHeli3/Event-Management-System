from rest_framework import generics, status
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Testimonials, QuestionAnswerForum
from .serializers import ViewTestimonialSerializer, AddTestimonialSerializer, QuestionAnswersSerializer, \
    AddQuestionSerializer, AddAnswerSerializer


class ViewTestimonials(generics.GenericAPIView, mixins.ListModelMixin):
    """
    class for viewing all the testimonials
    """
    serializer_class = ViewTestimonialSerializer
    queryset = Testimonials.objects.all().order_by('-post_date_time')

    def get(self, request):
        return self.list(request)


class AddTestimonials(generics.GenericAPIView, mixins.CreateModelMixin):
    """
    class for adding a testimonial
    """

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


class QuestionAnswersView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    class to view question and answers
    """

    serializer_class = QuestionAnswersSerializer
    queryset = QuestionAnswerForum.objects.all()

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


class AddAnswerView(generics.GenericAPIView, mixins.UpdateModelMixin):
    """
    class for adding an answer to a posted question
    """

    # serializer_class = AddAnswerSerializer
    # queryset = QuestionAnswerForum.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request):
        serializer = AddAnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
