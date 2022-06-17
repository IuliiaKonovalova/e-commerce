"""Test Inventory URLs."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from inventory.views import (
    ProductsListView,

)


class TestUrls(SimpleTestCase):
    """Test Inventory URLs."""

    def test_product_list_url(self):
        """Test product list url."""
        url = reverse('products_list')
        self.assertEquals(resolve(url).func.view_class, ProductsListView)

