"""Admin for orders."""
from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin for the Order model."""
    list_display = (
        'user',
        'full_name',
        'order_key',
        'total_paid',
        'billing_status',
        'status',
    )
    list_filter = (
        'billing_status',
        'status',
    )
    search_fields = (
        'user',
        'full_name',
        'email',
        'phone',
        'address1',
        'address2',
        'country',
        'county_region_state',
        'city',
        'zip_code',
        'order_key',
        'total_paid',
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin for the OrderItem model."""
    list_display = (
        'order',
        'product_inventory',
        'quantity',
    )
    list_filter = (
        'order',
        'product_inventory',
    )
    search_fields = (
        'order',
        'product_inventory',
        'quantity',
    )
    ordering = ('order',)
