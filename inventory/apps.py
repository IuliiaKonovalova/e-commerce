"""Apps for inventory app"""
from django.apps import AppConfig
from django.db.models.signals import post_save


class InventoryConfig(AppConfig):
    """AppConfig for inventory app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'
