"""Apps.py for the reviews app."""
from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """Config for the reviews app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
