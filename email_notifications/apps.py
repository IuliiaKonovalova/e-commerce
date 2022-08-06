"""Apps for the email_notifications app."""
from django.apps import AppConfig


class EmailNotificationsConfig(AppConfig):
    """Config for email_notifications app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'email_notifications'
