"""Admin for email_notifications."""
from django.contrib import admin
from .models import EmailNewsNotification


admin.site.register(EmailNewsNotification)
class EmailNewsNotificationAdmin(admin.ModelAdmin):
    """Admin for email news notifications."""
    list_display = ('email_name', 'content', 'created_at')
    list_filter = ('email_name',)
    search_fields = ('email_name',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['send_email']
