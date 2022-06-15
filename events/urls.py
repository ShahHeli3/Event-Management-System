from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ViewTestimonials, TestimonialsViewSet, QuestionAnswersView, AddQuestionView, AddAnswerView


router = DefaultRouter()
router.register('testimonial', TestimonialsViewSet, basename='testimonial')

urlpatterns = [
    path('testimonials/', ViewTestimonials.as_view(), name='testimonials'),
    path('question_answer/', QuestionAnswersView.as_view(), name='question_answer'),
    path('add_question/', AddQuestionView.as_view(), name='add_question'),
    path('add_answer/<int:id>/', AddAnswerView.as_view(), name='add_answer'),
] + router.urls

