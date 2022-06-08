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


class Profile(models.Model):
    """Model for the profiles."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='User',
        help_text=(
            'format: required, unique=True'
        )
    )
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='First name',
        help_text=(
            'format: not required, max_length=50'
        )
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Last name',
        help_text=(
            'format: not required, max_length=50'
        )
    )
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name='Birthday',
        help_text=(
            'format: not required'
        )
    )
    avatar = CloudinaryField(
        'avatar',
        folder='avatars',
        blank=True,
        null=True,
    )
    subscription = models.BooleanField(
        default=False,
        verbose_name='Subscription',
        help_text=(
            'format: not required'
        )
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        default=1,
        verbose_name='Role',
        help_text=(
            'format: not required'
        )
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at',
    )

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        if self.first_name:
            return self.first_name
        return self.user.username

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/images/default_avatar.svg'
