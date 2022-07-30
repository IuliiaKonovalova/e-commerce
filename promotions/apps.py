"""Apps.py for promotions app."""
from django.apps import AppConfig


class PromotionsConfig(AppConfig):
    """Config for promotions app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'promotions'
