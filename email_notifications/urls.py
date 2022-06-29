"""Urls for the email_notifications app."""
from django.urls import path
from .views import (
    EmailStockNotificationFormAJAX,
)


urlpatterns = [
    path(
        'add_to_stock_email_notification/',
        EmailStockNotificationFormAJAX.as_view(),
        name='add_to_stock_email_notification',
    ),
]