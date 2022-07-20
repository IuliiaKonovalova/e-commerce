"""Test for orders' urls."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from orders.views import (
    OrdersView,
    OrderDetailsView,
    UpdateOrderStatusAJAXView,
    AddOrderAJAXView,
    EditOrderView,
    DeleteOrderView,
    EditOrderItemView,
    DeleteOrderItemView,
    UserOrdersView,
    UserOrderDetailsView,
)


class TestUrls(SimpleTestCase):
    """Test for orders' urls."""
    def test_orders_url(self):
        """Test orders url."""
        url = reverse('orders')
        self.assertEquals(resolve(url).func.view_class, OrdersView)

    def test_order_details_url(self):
        """Test order details url."""
        url = reverse('order_details', kwargs={'order_id': 1})
        self.assertEquals(resolve(url).func.view_class, OrderDetailsView)

    def test_update_order_status_url(self):
        """Test update order status url."""
        url = reverse('update_order_status')
        self.assertEquals(
            resolve(url).func.view_class,
            UpdateOrderStatusAJAXView
        )

    def test_add_order_url(self):
        """Test add order url."""
        url = reverse('add')
        self.assertEquals(resolve(url).func.view_class, AddOrderAJAXView)

    def test_user_orders_url(self):
        """Test user orders url."""
        url = reverse('my_orders', kwargs={'user': 'test'})
        self.assertEquals(resolve(url).func.view_class, UserOrdersView)

    def test_user_order_details_url(self):
        """Test user order details url."""
        url = reverse(
            'my_order_details',
            kwargs={'user': 'test', 'order_number': 1}
        )
        self.assertEquals(resolve(url).func.view_class, UserOrderDetailsView)

    def test_edit_order_url(self):
        """Test edit order url."""
        url = reverse('edit', kwargs={'order_id': 1})
        self.assertEquals(resolve(url).func.view_class, EditOrderView)

    def test_delete_order_url(self):
        """Test delete order url."""
        url = reverse('delete', kwargs={'order_id': 1})
        self.assertEquals(resolve(url).func.view_class, DeleteOrderView)

    def test_edit_order_item_url(self):
        """Test edit order item url."""
        url = reverse('edit_order_item', kwargs={'order_item_id': 1})
        self.assertEquals(resolve(url).func.view_class, EditOrderItemView)

    def test_delete_order_item_url(self):
        """Test delete order item url."""
        url = reverse('delete_order_item', kwargs={'order_item_id': 1})
        self.assertEquals(resolve(url).func.view_class, DeleteOrderItemView)
