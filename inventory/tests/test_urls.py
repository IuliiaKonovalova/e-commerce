"""Test Inventory URLs."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from inventory.views import (
    ProductsListView,
    ProductDetailView,
)


class TestUrls(SimpleTestCase):
    """Test Inventory URLs."""

    def test_product_list_url(self):
        """Test product list url."""
        url = reverse('products_list')
        self.assertEquals(resolve(url).func.view_class, ProductsListView)

    def test_product_detail_url(self):
        """Test product detail url."""
        url = reverse('product_detail', kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, ProductDetailView)
