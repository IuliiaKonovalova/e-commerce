"""Test for personnel/urls.py"""
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from personnel.views import (
    ProductsTableView,
    ProductFullDetailView,
    AddProductView,
    EditProductView,
    AddImageToProductAJAXView,
    EditImageToProductAJAXView,
    DeleteImageToProductAJAXView,
    ProductInventoryDetailsView,
    AddProductInventoryDetailsView,
    GetTypeAttributeAJAXView,
    ProductInventoryCreateAJAXView,
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

    def test_edit_product_url(self):
        """Test the edit product url."""
        url = reverse('edit_product', kwargs={'pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            EditProductView
        )

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

    def test_delete_product_image_url(self):
        """Test the delete product image url."""
        url = reverse('delete_product_image')
        self.assertEquals(
            resolve(url).func.view_class,
            DeleteImageToProductAJAXView
        )

    def test_product_inventory_details_url(self):
        """Test the product inventory details url."""
        url = reverse(
            'product_inventory_details',
            kwargs={'pk': 1, 'inventory_pk': 1}
        )
        self.assertEquals(
            resolve(url).func.view_class,
            ProductInventoryDetailsView
        )

    def test_add_product_inventory_details_url(self):
        """Test the add product inventory details url."""
        url = reverse(
            'add_product_inventory_details',
            kwargs={'pk': 1}
        )
        self.assertEquals(
            resolve(url).func.view_class,
            AddProductInventoryDetailsView
        )

    def test_get_type_attribute_url(self):
        """Test the get type attribute url."""
        url = reverse('get_type_attribute')
        self.assertEquals(
            resolve(url).func.view_class,
            GetTypeAttributeAJAXView
        )

    def test_product_inventory_create_url(self):
        """Test the product inventory create url."""
        url = reverse('product_inventory_create')
        self.assertEquals(
            resolve(url).func.view_class,
            ProductInventoryCreateAJAXView
        )
