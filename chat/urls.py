from django.urls import path

from .views import UserValidationView, GetEventManagers, GetVendors

urlpatterns = [
    path('user_validation/', UserValidationView.as_view(), name='user_validation'),
    path('get_event_manager/', GetEventManagers.as_view(), name='get_event_manager'),
    path('get_vendor/', GetVendors.as_view(), name='get_vendor'),
]
