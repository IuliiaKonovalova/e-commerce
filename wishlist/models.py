"""Models for the Wishlist app."""
from django.db import models
from inventory.models import Product
from profiles.models import User


class Wishlist(models.Model):
    """Model for a wishlist."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name='wishlist'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    class Meta:
        """Meta class for the Wishlist model."""
        ordering = ['-created_at']
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        """Return the string representation of the model."""
        return str(self.user) + '\'s wishlist'

    def add_to_wishlist(self, product):
        """Add a product to the wishlist."""
        # check that product is not already in the wishlist
        if product not in self.products.all():
            self.products.add(product)
            return True
        return False

    def remove_from_wishlist(self, product):
        """Remove a product from the wishlist."""
        # check that product is in the wishlist
        if product in self.products.all():
            self.products.remove(product)
            return True
        return False

    def remove_all_from_wishlist(self):
        """Remove all products from the wishlist."""
        self.products.clear()
        return True

    def get_products(self):
        """Return the products in the wishlist."""
        return self.products.all()
