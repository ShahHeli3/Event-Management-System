from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from constants import SUCCESSFUL_REGISTRATION, SUCCESSFUL_LOGIN, LOGIN_ERROR, CHANGE_PASSWORD, \
    PASSWORD_RESET_EMAIL_SENT, PASSWORD_RESET_SUCCESSFUL, DELETE_PROFILE
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, ChangePasswordSerializer, \
    SendPasswordResetEmailSerializer, ResetPasswordSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
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
            return Response({'token': token, 'msg': SUCCESSFUL_REGISTRATION}, status=status.HTTP_201_CREATED)
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
                return Response({'token': token, 'msg': SUCCESSFUL_LOGIN}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': [LOGIN_ERROR]}}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    to change user password
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg': CHANGE_PASSWORD}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendResetPasswordEmailView(APIView):
    """
    to send a mail when user requests to change password
    """

    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response({'msg': PASSWORD_RESET_EMAIL_SENT}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """
    to reset user password
    """

    def post(self, request, user_id, token):
        serializer = ResetPasswordSerializer(data=request.data, context={'user_id': user_id, 'token': token})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg': PASSWORD_RESET_SUCCESSFUL}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    to view, update and delete user profile
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        try:
            return User.objects.get(id=request.user.id)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        user = self.get_object(request)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = self.get_object(request)
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = self.get_object(request)
        user.delete()
        return Response({'msg': DELETE_PROFILE}, status=status.HTTP_204_NO_CONTENT)
