import re
from django.core.exceptions import ValidationError

from constants import short_username, long_username, lowercase_username, blank_username, invalid_name, invalid_password


def validate_username(username):
    """
    Function to validate the username
    :param username: takes in username and validates it
    :return: validated username
    """
    if len(username) < 3:
        raise ValidationError(short_username)
    elif len(username) > 30:
        raise ValidationError(long_username)
    elif not username.islower():
        raise ValidationError(lowercase_username)
    elif " " in username:
        raise ValidationError(blank_username)
    else:
        return username


def validate_name(name):
    """
    Function to validate the first name and last name of the user
    :param name: takes in the first name or last name and validates it
    :return: validated name
    """
    if " " in name:
        raise ValidationError(invalid_name)
    elif name.isalpha():
        return name
    else:
        raise ValidationError(invalid_name)


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
        raise ValidationError(invalid_password)
