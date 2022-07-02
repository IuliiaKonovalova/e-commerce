"""Test for personnel/urls.py"""
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from personnel.views import (
    ProductsTableView,
)


class TestUrls(SimpleTestCase):
    """Tests for the personnel urls."""
    def test_products_table_url(self):
        """Test the products table url."""
        url = reverse('products_table')
        self.assertEquals(resolve(url).func.view_class, ProductsTableView)
