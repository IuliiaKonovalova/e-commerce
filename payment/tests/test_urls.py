"""Test payment urls."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from payment.views import (
    BasketView,
    order_placed,
    stripe_webhook
)


class TestUrls(SimpleTestCase):
    """Test payment urls."""

    def test_basket_url(self):
        """Test basket url."""
        url = reverse('payment')
        self.assertEquals(resolve(url).func, BasketView)


