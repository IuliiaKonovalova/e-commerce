"""Admin for wishlist."""
from django.contrib import admin
from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """Admin for the Wishlist model."""
    list_display = (
        'user',
        'created_at',
    )
    list_filter = (
        'user',
    )
    search_fields = (
        'user',
        'product',
        'created_at',
        'updated_at'
    )
