from django.urls import path
from .views import UserRegistrationView, UserLoginView, ChangePasswordView, SendResetPasswordEmailView, \
    ResetPasswordView, UserProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('send_reset_password_email/', SendResetPasswordEmailView.as_view(), name='send_reset_password_email'),
    path('reset_password/<user_id>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('profile/<int:id>/', UserProfileView.as_view(), name='profile'),
]

