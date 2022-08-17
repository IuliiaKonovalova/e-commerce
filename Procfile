release: python manage.py migrate
web: daphne ecommerce_project.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2 channel_layer