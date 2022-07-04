"""Test for personnel/urls.py"""
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from personnel.views import (
    ProductsTableView,
    ProductFullDetailView,
    AddProductView,
    AddImageToProductAJAXView,
    EditImageToProductAJAXView,
)


class TestUrls(SimpleTestCase):
    """Tests for the personnel urls."""
    def test_products_table_url(self):
        """Test the products table url."""
        url = reverse('products_table')
        self.assertEquals(resolve(url).func.view_class, ProductsTableView)

    def test_product_detail_url(self):
        """Test the product detail url."""
        url = reverse('product_detail_full', kwargs={'pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            ProductFullDetailView
        )

    def test_add_product_url(self):
        """Test the add product url."""
        url = reverse('add_product')
        self.assertEquals(resolve(url).func.view_class, AddProductView)

    def test_add_product_image_url(self):
        """Test the add product image url."""
        url = reverse('add_product_image')
        self.assertEquals(
            resolve(url).func.view_class,
            AddImageToProductAJAXView
        )

    def test_edit_product_image_url(self):
        """Test the edit product image url."""
        url = reverse('edit_product_image')
        self.assertEquals(
            resolve(url).func.view_class,
            EditImageToProductAJAXView
        )
