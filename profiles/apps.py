"""Apps for the profiles app."""
from django.apps import AppConfig
from django.db.models.signals import post_save


class ProfilesConfig(AppConfig):
    """Config for the profiles app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        from profiles.signals import create_profile
        from django.contrib.auth.models import User
        post_save.connect(create_profile, sender=User)
        from profiles.signals import save_profile
        post_save.connect(save_profile, sender=User)
