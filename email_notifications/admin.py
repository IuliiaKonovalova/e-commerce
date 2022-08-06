"""Admin for email_notifications."""
from django.contrib import admin
from .models import EmailNewsNotification, StockEmailNotification


@admin.register(EmailNewsNotification)
class EmailNewsNotificationAdmin(admin.ModelAdmin):
    """Admin for email news notifications."""
    list_display = ('email_name', 'content', 'created_at')
    list_filter = ('email_name',)
    search_fields = ('email_name',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['send_email']


@admin.register(StockEmailNotification)
class StockEmailNotification(admin.ModelAdmin):
    """Admin for product detail view."""
    list_display = (
        'user',
        'requested_product',
        'requested_quantity',
        'created_at',
        'answer_sent',
        'get_all_requested_attributes_values_objects'
    )
    list_filter = ('user', 'requested_product')
    search_fields = ('user', 'requested_product')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 25
