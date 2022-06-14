from django.urls import path

from .views import ViewTestimonials, AddTestimonials, QuestionAnswersView, AddQuestionView, AddAnswerView

urlpatterns = [
    path('testimonials/', ViewTestimonials.as_view(), name='testimonials'),
    path('add_testimonials/', AddTestimonials.as_view(), name='add_testimonials'),
    path('question_answer/', QuestionAnswersView.as_view(), name='question_answer'),
    path('add_question/', AddQuestionView.as_view(), name='add_question'),
    path('add_answer/', AddAnswerView.as_view(), name='add_answer'),
]

