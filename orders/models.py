"""Models for Orders app."""
import uuid
from django.db import models
from django.contrib.auth.models import User
from inventory.models import ProductInventory


class Order(models.Model):
    """Model for Order."""
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'shipped'
    COMPLETED = 'Completed'
    REFUNDED = 'Refunded'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (COMPLETED, 'Completed'),
        (REFUNDED, 'Refunded'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='order_user'
    )
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=100)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    county_region_state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.CharField(
        max_length=32, null=False, editable=False
    )
    billing_status = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return str(self.created) + ' - ' + str(self.order_key)

    def _generate_order_key(self):
        """Generate a random, unique order key using UUID"""
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """Override the save method to set the order key."""
        if not self.order_key:
            self.order_key = self._generate_order_key()
        super().save(*args, **kwargs)



