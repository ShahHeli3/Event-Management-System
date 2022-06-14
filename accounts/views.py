from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from constants import successful_registration, successful_login, login_error, change_password, \
    password_reset_email_sent, password_reset_successful, successful_logout
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, ChangePasswordSerializer, \
    SendPasswordResetEmailSerializer, ResetPasswordSerializer, UserProfileSerializer
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    """
    function to get refresh and access tokens for user authentication
    :param user: takes in the verified user
    :return: refresh token and access token
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    """
    to register a new user
    """

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': successful_registration}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    to login a user
    """

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)

            if user:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': successful_login}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': [login_error]}}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    to change user password
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg': change_password}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendResetPasswordEmailView(APIView):
    """
    to send a mail when user requests to change password
    """

    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response({'msg': password_reset_email_sent}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """
    to reset user password
    """

    def post(self, request, user_id, token):
        serializer = ResetPasswordSerializer(data=request.data, context={'user_id': user_id, 'token': token})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg': password_reset_successful}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    to view, update and delete user profile
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        user = self.get_object(id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        user = self.get_object(id)
        serializer = UserProfileSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = self.get_object(id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserLogOutView(APIView):
    """
    for user logout
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({'msg': successful_logout}, status=status.HTTP_200_OK)
