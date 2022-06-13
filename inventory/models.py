"""Models for the inventory app."""
from django.db import models
from cloudinary.models import CloudinaryField


class Category(models.Model):
    """Category model"""
    name = models.CharField(
        max_length=100,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Category name',
        help_text='format: required, max_length=100'
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Category Slug',
        help_text='format: required, max_length=150'
    )
    is_active = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at'
    )
    class Meta:
        """Meta class for Category model"""
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        """String representation of Category model"""
        return self.name


class Tag(models.Model):
    """Tag model"""
    name = models.CharField(
        max_length=100,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Tag name',
        help_text='format: required, max_length=100'
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Tag Slug',
        help_text='format: required, max_length=150'
    )
    is_active = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at'
    )
    class Meta:
        """Meta class for Tag model"""
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        """String representation of Tag model"""
        return self.name


class Brand(models.Model):
    """Brand model"""
    name = models.CharField(
        max_length=100,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Brand name',
        help_text='format: required, max_length=100'
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=True,
        blank=False,
        verbose_name='Brand Slug',
        help_text='format: required, max_length=150'
    )
    description = models.TextField(
        max_length=500,
        null=False,
        blank=False,
        verbose_name='Brand description',
        help_text='format: required, max_length=500'
    )
    is_active = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at'
    )
    class Meta:
        """Meta class for Brand model"""
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        ordering = ['name']

    def __str__(self):
        """String representation of the model"""
        return self.name