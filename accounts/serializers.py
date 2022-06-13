from rest_framework import serializers
from .models import User
import re
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util


def validate_password(password):
    """
    Function to validate password
    :param password: takes in password and validates it
    :return: validated password
    """
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"

    if re.fullmatch(reg, password):
        return password
    else:
        raise ValidationError("Invalid password. Password must contain atleast one uppercase alphabet, one lowercase "
                              "alphabet, one digit, one special character and must be 8 to 20 characters in length.")


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'f_name', 'l_name', 'password', 'password2', 'contact_num', 'profile_image']
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")

        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            # print("encoded uid--->", user_id)
            token = PasswordResetTokenGenerator().make_token(user)
            # print("token--->", token)
            link = 'http://localhost:3000/api/user/reset/'+user_id+'/'+token
            # print("link--->", link)

            # send mail
            body = 'Click the following link to Reset your Password '+link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            Util.send_mail(data)

            return attrs
        else:
            raise ValidationError('You are not a registered user. Please enter a registered Email ID')


class ResetPasswordSerializer(serializers.Serializer):

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
                raise serializers.ValidationError("Password and Confirm Password doesn't match")

            id = smart_str(urlsafe_base64_decode(user_id))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError("Token is invalid or expired")

            user.set_password(password)
            user.save()
            return attrs

        except DjangoUnicodeDecodeError:
            PasswordResetTokenGenerator().check_token((user, token))
            raise ValidationError("Token is invalid or expired")


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username', 'f_name', 'l_name', 'contact_num', 'profile_image']
