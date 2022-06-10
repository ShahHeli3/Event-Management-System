from django.urls import path
from .views import UserRegistrationView, UserLoginView, ChangePasswordView

# UserProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('changepassword/', ChangePasswordView.as_view(), name='changepassword'),
    # path('profile/', UserProfileView.as_view(), name='profile'),
]

