from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ViewTestimonials, TestimonialsViewSet, QuestionAnswersView, AddQuestionView, AddAnswerView, \
    EventCategoriesViewSet, GetEventsView, EventsViewSet

router = DefaultRouter()
router.register('testimonial', TestimonialsViewSet, basename='testimonial')
router.register('event_categories', EventCategoriesViewSet, basename='event_categories')
router.register('events', EventsViewSet, basename='events')

urlpatterns = [
    path('view_testimonials/', ViewTestimonials.as_view(), name='view_testimonials'),
    path('question_answer/', QuestionAnswersView.as_view(), name='question_answer'),
    path('add_question/', AddQuestionView.as_view(), name='add_question'),
    path('add_answer/<int:id>/', AddAnswerView.as_view(), name='add_answer'),
    path('view_events/', GetEventsView.as_view(), name='view_events'),
] + router.urls

