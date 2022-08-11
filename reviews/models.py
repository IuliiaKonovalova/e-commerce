"""Models for reviews app"""
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from inventory.models import Product
from orders.models import Order


class Review(models.Model):
    """Review model."""
    STAR_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    rating = models.CharField(
        max_length=20,
        choices=STAR_CHOICES,
        default=1,
    )
    comment = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of model."""
        return f'{self.user.username} - {self.product.name} - {self.rating}'

    class Meta:
        """Meta class."""
        ordering = ['-created_at']


class ReviewImage(models.Model):
    """Review image model."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = CloudinaryField(
        'review_image',
        null=True,
        blank=True,
    )

    def __str__(self):
        """Return string representation of model."""
        return f'{self.review.user.username} - {self.review.product.name}'

    class Meta:
        """Meta class."""
        ordering = ['-id']

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return False
