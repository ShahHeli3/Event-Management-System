from event_management import settings

if settings.DEBUG:
    password_reset_link = 'http://localhost:8000/api/user/reset_password/'
else:
    password_reset_link = 'https://heli-event-management.herokuapp.com/api/user/reset_password/'

# user manager error
user_manager = "User must have an email address"

# passwords error
passwords_does_not_match = "Password and Confirm Password doesn't match"
current_password_check = "Current password is invalid"

# reset email error
reset_email_body = "Click the following link to Reset your Password "
reset_email_user_error = "You are not a registered user. Please enter a registered Email ID"

# token error
token_error = "Token is invalid or expired"

# validation errors
# username validation errors
short_username = "Username too short.Please enter a username of at least 3 characters."
long_username = "Username too long.Please enter a username of not greater than 30 characters."
lowercase_username = "Username should consists of lower case alphabets only."
blank_username = "Username cannot contain spaces."

# name validations error
invalid_name = "Input name is invalid. Please enter a valid name"

# password validation error
invalid_password = "Invalid password. Password must contain atleast one uppercase alphabet, one lowercase alphabet, " \
                   "one digit, one special character and must be 8 to 20 characters in length."


# response messages
successful_registration = "Registration successful"
successful_login = "Login Successful"
login_error = "Email or password is not valid"
change_password = "Password Changed Successfully"
password_reset_email_sent = "A link to reset your password has been sent to your email ID. Please check your email"
password_reset_successful = "Password Reset Successful"
