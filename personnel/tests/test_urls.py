"""Test for personnel/urls.py"""
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from personnel.views import (
    ProductsTableView,
    ProductFullDetailView,
    AddProductView,
    EditProductView,
    DeleteProductView,
    AddImageToProductAJAXView,
    EditImageToProductAJAXView,
    DeleteImageToProductAJAXView,
    ProductInventoryDetailsView,
    AddProductInventoryDetailsView,
    GetTypeAttributeAJAXView,
    ProductInventoryCreateAJAXView,
    EditProductInventoryView,
    UpdateProductInventoryAJAXView,
    DeleteProductInventoryView,
    ProductInventoriesTableView,
    CategoriesTableView,
    AddCategoryView,
    EditCategoryView,
    DeleteCategoryView,
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

    def test_delete_product_url(self):
        """Test the delete product url."""
        url = reverse('delete_product', kwargs={'pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            DeleteProductView
        )
        self.assertEquals(resolve(url).kwargs['pk'], 1)

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

    def test_edit_product_inventory_url(self):
        """Test the edit product inventory url."""
        url = reverse(
            'edit_product_inventory',
            kwargs={'pk': 1, 'inventory_pk': 1}
        )
        self.assertEquals(
            resolve(url).func.view_class,
            EditProductInventoryView
        )

    def test_update_product_inventory_url(self):
        """Test the update product inventory url."""
        url = reverse('product_inventory_update')
        self.assertEquals(
            resolve(url).func.view_class,
            UpdateProductInventoryAJAXView
        )

    def test_delete_product_inventory_url(self):
        """Test the delete product inventory url."""
        url = reverse(
            'delete_product_inventory',
            kwargs={'pk': 1, 'inventory_pk': 1}
        )
        self.assertEquals(
            resolve(url).func.view_class,
            DeleteProductInventoryView
        )

    def test_product_inventories_table_url(self):
        """Test the product inventories table url."""
        url = reverse('product_inventories_table')
        self.assertEquals(
            resolve(url).func.view_class,
            ProductInventoriesTableView
        )

    def test_categories_table_url(self):
        """Test the categories table url."""
        url = reverse('categories_table')
        self.assertEquals(
            resolve(url).func.view_class,
            CategoriesTableView
        )

    def test_add_category_url(self):
        """Test the add category url."""
        url = reverse('add_category')
        self.assertEquals(
            resolve(url).func.view_class,
            AddCategoryView
        )

    def test_edit_category_url(self):
        """Test the edit category url."""
        url = reverse('edit_category', kwargs={'category_pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            EditCategoryView
        )

    def test_delete_category_url(self):
        """Test the delete category url."""
        url = reverse('delete_category', kwargs={'category_pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            DeleteCategoryView
        )
        self.assertEquals(resolve(url).kwargs['category_pk'], 1)
