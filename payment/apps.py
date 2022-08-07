"""Apps for payment app"""
from django.apps import AppConfig


class PaymentConfig(AppConfig):
    """AppConfig for payment app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
