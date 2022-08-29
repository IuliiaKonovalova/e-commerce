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
    phone = models.CharField(max_length=100, blank=True)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100)
    county_region_state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_number = models.CharField(
        max_length=32, null=False, editable=False
    )
    order_key = models.CharField(max_length=200, blank=True, null=True)
    billing_status = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.order_number)

    def _generate_order_number(self):
        """Generate a random, unique order number using UUID"""
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """Override the save method to set the order number."""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def get_order_items(self):
        """Get the order items for the order."""
        items = OrderItem.objects.filter(order=self)
        return items


class OrderItem(models.Model):
    """Model for OrderItem."""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_item'
    )
    product_inventory = models.ForeignKey(
        ProductInventory,
        on_delete=models.CASCADE,
        related_name='order_item_inventory'
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
