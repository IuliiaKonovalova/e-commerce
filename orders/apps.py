"""Apps.py for orders app."""
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """Config for orders app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
