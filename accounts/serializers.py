from rest_framework import serializers
from .models import User
import re
from django.core.exceptions import ValidationError


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

# class UserProfileSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'name']
