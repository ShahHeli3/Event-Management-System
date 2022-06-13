from django.urls import path
from .views import ViewTestimonials, AddTestimonials

urlpatterns = [
    path('testimonials/', ViewTestimonials.as_view(), name='testimonials'),
    path('add_testimonials/', AddTestimonials.as_view(), name='add_testimonials'),
]

