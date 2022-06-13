import re
from django.core.exceptions import ValidationError


def validate_username(username):
    """
    Function to validate the username
    :param username: takes in username and validates it
    :return: validated username
    """
    if len(username) < 3:
        raise ValidationError("Username too short.Please enter a username of atleast 3 characters.")
    elif len(username) > 30:
        raise ValidationError("Username too long.Please enter a username of not greater than 30 characters.")
    elif not username.islower():
        raise ValidationError("Username should consists of lower case alphabets only.")
    elif " " in username:
        raise ValidationError("Username cannot contain spaces.")
    else:
        return True


def validate_name(name):
    """
    Function to validate the first name and last name of the user
    :param name: takes in the first name or last name and validates it
    :return: validated name
    """
    if " " in name:
        raise ValidationError(f"{name} cannot contain spaces.")
    elif name.isalpha():
        return name
    else:
        raise ValidationError(f"{name} is invalid. Enter a valid name")


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
