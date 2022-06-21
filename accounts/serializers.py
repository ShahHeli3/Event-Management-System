from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from constants import PASSWORD_DOES_NOT_MATCH, CURRENT_PASSWORD_CHECK, PASSWORD_RESET_LINK, RESET_EMAIL_BODY, \
    RESET_EMAIL_USER_ERROR, TOKEN_ERROR
from utils import Util
from .models import User
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .validations import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    serializer to register user
    """
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password2', 'contact_number', 'profile_image']

        # for reference (another way of mentioning new field)
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError(PASSWORD_DOES_NOT_MATCH)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """
    serializer to login user
    """
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class ChangePasswordSerializer(serializers.Serializer):
    """
    serializer to change user password
    """
    current_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        current_password = attrs.get('current_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if not check_password(current_password, user.password):
            raise serializers.ValidationError(CURRENT_PASSWORD_CHECK)

        if password != password2:
            raise serializers.ValidationError(PASSWORD_DOES_NOT_MATCH)

        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    """
    serializer to send a mail for password reset
    """
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = PASSWORD_RESET_LINK+user_id+'/'+token

            # send mail
            body = RESET_EMAIL_BODY +link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': [user.email]
            }
            Util.send_mail(data)

            return attrs
        else:
            raise ValidationError(RESET_EMAIL_USER_ERROR)


class ResetPasswordSerializer(serializers.Serializer):
    """
    serializer to reset password
    """

    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            user_id = self.context.get('user_id')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError(PASSWORD_DOES_NOT_MATCH)

            id = smart_str(urlsafe_base64_decode(user_id))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError(TOKEN_ERROR)

            user.set_password(password)
            user.save()
            return attrs

        except DjangoUnicodeDecodeError:
            raise ValidationError(TOKEN_ERROR)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    serializer for user profile operations
    """

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'contact_number', 'profile_image']
