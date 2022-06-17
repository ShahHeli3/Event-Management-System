from event_management import settings

if settings.DEBUG:
    PASSWORD_RESET_LINK = 'http://localhost:8000/api/user/reset_password/'
else:
    PASSWORD_RESET_LINK = 'https://heli-event-management.herokuapp.com/api/user/reset_password/'

# user manager error
USER_MANAGER = "User must have an email address"

# passwords error
PASSWORD_DOES_NOT_MATCH = "Password and Confirm Password doesn't match"
CURRENT_PASSWORD_CHECK = "Current password is invalid"

# reset email error
RESET_EMAIL_BODY = "Click the following link to Reset your Password "
RESET_EMAIL_USER_ERROR = "You are not a registered user. Please enter a registered Email ID"

# token error
TOKEN_ERROR = "Token is invalid or expired"

# validation errors
# username validation errors
SHORT_USERNAME = "Username too short.Please enter a username of at least 3 characters."
LONG_USERNAME = "Username too long.Please enter a username of not greater than 30 characters."
LOWERCASE_USERNAME = "Username should consists of lower case alphabets only."
BLANK_USERNAME = "Username cannot contain spaces."

# name validations error
INVALID_NAME = "Input name is invalid. Please enter a valid name"

# password validation error
INVALID_PASSWORD = "Invalid password. Password must contain atleast one uppercase alphabet, one lowercase alphabet, " \
                   "one digit, one special character and must be 8 to 20 characters in length."


# response messages
SUCCESSFUL_REGISTRATION = "Registration successful"
SUCCESSFUL_LOGIN = "Login Successful"
LOGIN_ERROR = "Email or password is not valid"
CHANGE_PASSWORD = "Password Changed Successfully"
PASSWORD_RESET_EMAIL_SENT = "A link to reset your password has been sent to your email ID. Please check your email"
PASSWORD_RESET_SUCCESSFUL = "Password Reset Successful"
DELETE_PROFILE = "Profile deleted"
ACCESS_DENIED = "Access Denied. You don't have access to other user's data"
DELETE_TESTIMONIAL = "Your testimonial has been deleted successfully"
DELETE_REVIEW = "Your event review has been deleted successfully"