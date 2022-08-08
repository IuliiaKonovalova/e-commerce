"""Apps.py for home app"""
from django.apps import AppConfig


class HomeConfig(AppConfig):
    """AppConfig for home app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
