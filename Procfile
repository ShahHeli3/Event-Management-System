web: gunicorn event_management.wsgi
web: daphne event_management.asgi:application
worker: python manage.py runworker --settings=event_management.settings -v2