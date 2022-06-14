import re
from django.core.exceptions import ValidationError

from constants import SHORT_USERNAME, LONG_USERNAME, LOWERCASE_USERNAME, BLANK_USERNAME, INVALID_NAME, INVALID_PASSWORD


def validate_username(username):
    """
    Function to validate the username
    :param username: takes in username and validates it
    :return: validated username
    """
    if len(username) < 3:
        raise ValidationError(SHORT_USERNAME)
    elif len(username) > 30:
        raise ValidationError(LONG_USERNAME)
    elif not username.islower():
        raise ValidationError(LOWERCASE_USERNAME)
    elif " " in username:
        raise ValidationError(BLANK_USERNAME)
    else:
        return username


def validate_name(name):
    """
    Function to validate the first name and last name of the user
    :param name: takes in the first name or last name and validates it
    :return: validated name
    """
    if " " in name:
        raise ValidationError(INVALID_NAME)
    elif name.isalpha():
        return name
    else:
        raise ValidationError(INVALID_NAME)


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
        raise ValidationError(INVALID_PASSWORD)
