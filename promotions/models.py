"""Models for the promotions app."""
from django.db import models
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from inventory.models import ProductInventory

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Promotion(models.Model):
    """Model for promotions."""
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Name',
        help_text='Name of the promotion.'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Slug',
        help_text='Slug of the promotion.'
    )
    description = models.TextField(
        max_length=700,
        null=False,
        blank=False,
        verbose_name='Promotion description',
        help_text='format: required, max_length=700'
    )
    promotion_code = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Promotion code',
        help_text='Promotion code.'
    )
    promotion_reduction = models.DecimalField(
        max_digits=3,
        decimal_places=0,
        default=Decimal(0),
        validators=PERCENTAGE_VALIDATOR,
    )
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField(
        verbose_name='Start date',
    )
    end_date = models.DateTimeField(
        verbose_name='End date',
    )
    products_inventory_in_promotion = models.ManyToManyField(
        ProductInventory,
        blank=True,
        related_name='products_promotions',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
        help_text='Date and time of creation.'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at',
        help_text='Date and time of last update.'
    )

    class Meta:
        """Meta class for promotions."""
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'
        ordering = ['-created_at']

    def __str__(self):
        """Return the name of the promotion."""
        return self.name

    def save(self, *args, **kwargs):
        """Save the promotion."""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_promotion_code(self):
        """Return the promotion code."""
        return self.promotion_code

    def is_active_now(self):
        """Return whether the promotion is active now."""
        start_date = self.start_date.replace(tzinfo=None)
        end_date = self.end_date.replace(tzinfo=None)
        return (
            self.active and start_date < datetime.now() < end_date
        )

    def is_active_soon(self):
        """Return whether the promotion is active soon."""
        start_date = self.start_date.replace(tzinfo=None)
        end_date = self.end_date.replace(tzinfo=None)
        return (
            self.active and start_date < datetime.now() + timedelta(
                days=7
            ) < end_date
        )

    def get_products_in_promotion(self):
        """Return the products in the promotion."""
        return self.products_inventory_in_promotion.all()
