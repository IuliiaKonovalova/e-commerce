"""Models for the profiles app."""
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Role(models.Model):
    """Model for the roles."""
    name = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Role name',
        help_text=(
            'format: required, max_length=50, unique=True, blank=False'
        )
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Role description',
        help_text=(
            'format: not required, max_length=500'
        )
    )

    def __str__(self):
        """Return the name of the role."""
        return self.name