from django.urls import path
from .views import UserRegistrationView, UserLoginView, ChangePasswordView

# UserProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    # path('profile/', UserProfileView.as_view(), name='profile'),
]

