"""Models for the profiles app."""
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from datetime import date


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

    @property
    def age(self):
        if self.birthday:
            today = date.today()
            birthday = (
                today.year -
                self.birthday.year -
                (
                    (today.month, today.day) < (
                        self.birthday.month, self.birthday.day
                    )
                )
            )
            if birthday < 0:
                return 'Invalid birthday'
            return birthday
        return None


class Address(models.Model):
    """Model for the addresses."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='User',
        help_text=(
            'format: required'
        )
    )
    country = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Country',
        help_text=(
            'format: required, max_length=50'
        )
    )
    county_region = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='County/region',
        help_text=(
            'format: required, max_length=50'
        )
    )
    city = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='City',
        help_text=(
            'format: required, max_length=50'
        )
    )
    address_line = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Address line',
        help_text=(
            'format: required, max_length=150'
        )
    )
    zip_code = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        verbose_name='Zip code',
        help_text=(
            'format: required, max_length=10'
        )
    )
    phone_number = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        verbose_name='Phone',
        help_text=(
            'format: required, max_length=15'
        )
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name='Is primary',
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
        """Return the address line."""
        return f'{self.user.username} - {self.zip_code} - {self.is_primary}'

    def save(self, *args, **kwargs):
        """Check if there is a primary address."""
        super().save(*args, **kwargs)
        if self.is_primary:
            for address in self.user.addresses.all().exclude(id=self.id):
                address.is_primary = False
                address.save()
