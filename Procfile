web: gunicorn event_management.wsgi
daphne -p 8000 event_management.asgi:application
worker: python manage.py runworker --settings=event_management.settings -v2