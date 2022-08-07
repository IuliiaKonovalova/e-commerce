"""Test for personnel/urls.py"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
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
    BrandsTableView,
    BrandDetailView,
    AddBrandView,
    EditBrandView,
    DeleteBrandView,
    TagsTableView,
    TagDetailView,
    AddTagView,
    EditTagView,
    DeleteTagView,
    StockView,
    AddStockView,
    UpdateStockView,
    DeleteStockView,
    ProductTypesListView,
    AddProductTypeView,
    UpdateProductTypeView,
    DeleteProductTypeView,
    AttributesListView,
    AddAttributeView,
    EditAttributeView,
    DeleteAttributeView,
    AttributeValuesListView,
    AddAttributeValueView,
    EditAttributeValueView,
    DeleteAttributeValueView,
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

    def test_brands_table_url(self):
        """Test the brands table url."""
        url = reverse('brands_table')
        self.assertEquals(
            resolve(url).func.view_class,
            BrandsTableView
        )

    def test_brand_detail_url(self):
        """Test the brand detail url."""
        url = reverse('brand_detail', kwargs={'brand_pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            BrandDetailView
        )

    def test_add_brand_url(self):
        """Test the add brand url."""
        url = reverse('add_brand')
        self.assertEquals(
            resolve(url).func.view_class,
            AddBrandView
        )

    def test_edit_brand_url(self):
        """Test the edit brand url."""
        url = reverse('edit_brand', kwargs={'brand_pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            EditBrandView
        )

    def test_delete_brand_url(self):
        """Test the delete brand url."""
        url = reverse('delete_brand', kwargs={'brand_pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            DeleteBrandView
        )
        self.assertEquals(resolve(url).kwargs['brand_pk'], 1)

    def test_tags_table_url(self):
        """Test the tags table url."""
        url = reverse('tags_table')
        self.assertEquals(
            resolve(url).func.view_class,
            TagsTableView
        )

    def test_tag_detail_url(self):
        """Test the tag detail url."""
        url = reverse('tag_detail', kwargs={'tag_pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            TagDetailView
        )

    def test_add_tag_url(self):
        """Test the add tag url."""
        url = reverse('add_tag')
        self.assertEquals(
            resolve(url).func.view_class,
            AddTagView
        )

    def test_edit_tag_url(self):
        """Test the edit tag url."""
        url = reverse('edit_tag', kwargs={'tag_pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            EditTagView
        )

    def test_delete_tag_url(self):
        """Test the delete tag url."""
        url = reverse('delete_tag', kwargs={'tag_pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            DeleteTagView
        )
        self.assertEquals(resolve(url).kwargs['tag_pk'], 1)

    def test_stock_url(self):
        """Test the stock table url."""
        url = reverse('stock')
        self.assertEquals(
            resolve(url).func.view_class,
            StockView
        )

    def test_add_stock_url(self):
        """Test the stock table url."""
        url = reverse('add_stock', kwargs={'pk': 1, 'inventory_pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            AddStockView
        )

    def test_update_stock_url(self):
        """Test the stock table url."""
        url = reverse(
            'update_stock',
            kwargs={'pk': 1, 'inventory_pk': 1, 'stock_pk': 1}
        )
        self.assertEquals(
            resolve(url).func.view_class,
            UpdateStockView
        )

    def test_delete_stock_url(self):
        """Test the stock table url."""
        url = reverse(
            'delete_stock',
            kwargs={'pk': 1, 'inventory_pk': 1, 'stock_pk': 1}
        )
        self.assertEquals(
            resolve(url).func.view_class,
            DeleteStockView
        )

    def test_product_types_table_url(self):
        """Test the product types table url."""
        url = reverse('product_types_table')
        self.assertEquals(
            resolve(url).func.view_class,
            ProductTypesListView
        )

    def test_add_product_type_url(self):
        """Test the add product type url."""
        url = reverse('add_product_type')
        self.assertEquals(
            resolve(url).func.view_class,
            AddProductTypeView
        )

    def test_edit_product_type_url(self):
        """Test the edit product type url."""
        url = reverse('edit_product_type', kwargs={'pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            UpdateProductTypeView
        )

    def test_delete_product_type_url(self):
        """Test the delete product type url."""
        url = reverse('delete_product_type', kwargs={'pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            DeleteProductTypeView
        )

    def test_attributes_table_url(self):
        """Test the attributes table url."""
        url = reverse('product_type_attributes')
        self.assertEquals(
            resolve(url).func.view_class,
            AttributesListView
        )

    def test_add_attribute_url(self):
        """Test the add attribute url."""
        url = reverse('add_attribute')
        self.assertEquals(
            resolve(url).func.view_class,
            AddAttributeView
        )

    def test_edit_attribute_url(self):
        """Test the edit attribute url."""
        url = reverse('edit_attribute', kwargs={'pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            EditAttributeView
        )

    def test_delete_attribute_url(self):
        """Test the delete attribute url."""
        url = reverse('delete_attribute', kwargs={'pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            DeleteAttributeView
        )

    def test_attribute_values_url(self):
        """Test the attribute values table url."""
        url = reverse('attribute_values')
        self.assertEquals(
            resolve(url).func.view_class,
            AttributeValuesListView
        )

    def test_add_attribute_value_url(self):
        """Test the add attribute value url."""
        url = reverse('add_attribute_value')
        self.assertEquals(
            resolve(url).func.view_class,
            AddAttributeValueView
        )

    def test_edit_attribute_value_url(self):
        """Test the edit attribute value url."""
        url = reverse('edit_attribute_value', kwargs={'pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            EditAttributeValueView
        )

    def test_delete_attribute_value_url(self):
        """Test the delete attribute value url."""
        url = reverse('delete_attribute_value', kwargs={'pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            DeleteAttributeValueView
        )
