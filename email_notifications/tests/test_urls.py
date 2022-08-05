"""Test for email_notifications/urls.py"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from email_notifications.views import (
    EmailStockNotificationFormAJAX,
    PromoEmailCreateView,
    StockRequestsListView,
)


class TestUrls(SimpleTestCase):
    """Test for email_notifications/urls.py"""

    def test_add_to_stock_email_notification_url(self):
        """Test for email_notifications/urls.py"""
        url = reverse('add_to_stock_email_notification')
        self.assertEquals(
            resolve(url).func.view_class, EmailStockNotificationFormAJAX
        )

    def test_add_promo_email_url(self):
        """Test for email_notifications/urls.py"""
        url = reverse('add_promo_email')
        self.assertEquals(
            resolve(url).func.view_class, PromoEmailCreateView
        )

    def test_stock_requests_list_url(self):
        """Test for email_notifications/urls.py"""
        url = reverse('stock_requests_list')
        self.assertEquals(
            resolve(url).func.view_class, StockRequestsListView
        )
