web: gunicorn event_management.wsgi
daphne event_management.asgi:application --port $PORT --bind 0.0.0.0
worker: python manage.py runworker --settings=event_management.settings -v2


