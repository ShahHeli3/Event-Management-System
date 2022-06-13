from event_management import settings

if settings.DEBUG:
    password_reset_link = 'http://localhost:8000/api/user/reset_password/'
else:
    password_reset_link = 'https://heli-event-management.herokuapp.com/api/user/reset_password/'