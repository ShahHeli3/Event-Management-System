from django.urls import path
from .views import UserValidationView, GetEventManagers, GetVendors, ChatRoom, rooms

urlpatterns = [
    path('', UserValidationView.as_view(), name='user_validation'),
    path('rooms/', rooms, name='rooms'),
    path('get_event_manager/', GetEventManagers.as_view(), name='get_event_manager'),
    path('get_vendor/', GetVendors.as_view(), name='get_vendor'),
    path('rooms/<str:room_name>/', ChatRoom.as_view(), name='room'),
]
