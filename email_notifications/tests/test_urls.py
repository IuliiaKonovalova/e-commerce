"""Test for email_notifications/urls.py"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from email_notifications.views import (
    EmailStockNotificationFormAJAX,
)


class TestUrls(SimpleTestCase):
    def test_add_to_stock_email_notification_url(self):
        url = reverse('add_to_stock_email_notification')
        self.assertEquals(
            resolve(url).func.view_class, EmailStockNotificationFormAJAX
        )
