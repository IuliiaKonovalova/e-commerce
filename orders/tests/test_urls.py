"""Test for orders' urls."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from orders.views import (
    OrdersView,

)


class TestUrls(SimpleTestCase):
    """Test for orders' urls."""
    def test_orders_url(self):
        """Test orders url."""
        url = reverse('orders')
        self.assertEquals(resolve(url).func.view_class, OrdersView)
