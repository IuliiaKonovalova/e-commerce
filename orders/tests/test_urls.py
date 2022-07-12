"""Test for orders' urls."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from orders.views import (
    OrdersView,
    AddOrderAJAXView,
    UserOrdersView,
)


class TestUrls(SimpleTestCase):
    """Test for orders' urls."""
    def test_orders_url(self):
        """Test orders url."""
        url = reverse('orders')
        self.assertEquals(resolve(url).func.view_class, OrdersView)

    def test_add_order_url(self):
        """Test add order url."""
        url = reverse('add')
        self.assertEquals(resolve(url).func.view_class, AddOrderAJAXView)

    def test_user_orders_url(self):
        """Test user orders url."""
        url = reverse('my_orders', kwargs={'user': 'test'})
        self.assertEquals(resolve(url).func.view_class, UserOrdersView)


