"""Test payment urls."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from payment.views import (
    BasketView,
    order_placed,
)


class TestUrls(SimpleTestCase):
    """Test payment urls."""

    def test_basket_url(self):
        """Test basket url."""
        url = reverse('payment')
        self.assertEquals(resolve(url).func, BasketView)

    def test_order_placed_url(self):
        """Test order placed url."""
        url = reverse('order_placed')
        self.assertEquals(resolve(url).func, order_placed)
