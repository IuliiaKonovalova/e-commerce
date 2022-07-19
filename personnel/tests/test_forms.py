"""Tests for the forms of the inventory app."""
from django.test import TestCase
from inventory.models import (
    Category,
    Tag,
    Brand,
    Product,
    ProductImage,
    ProductType,
    ProductAttribute,
    ProductAttributeValue,
    ProductInventory,
)
from personnel.forms import (
    CategoryForm,
    TagForm,
    BrandForm,
    ProductForm,
    ProductImageForm,
    ProductAttributeForm,
    ProductTypeForm,
    ProductAttributeValueForm,
    ProductInventoryForm,
    StockForm,
)


class TestForms(TestCase):
    """Tests for the forms of the inventory app."""
    def setUp(self):
        """Set up the test."""
        self.category1 = Category.objects.create(
            name='Clothing',
            slug='clothing',
            is_active=False,
        )
        self.category2 = Category.objects.create(
            name='Food',
            slug='food',
            is_active=True,
        )
        self.tag1 = Tag.objects.create(
            name='skirt',
            slug='skirt',
            is_active=True,
        )
        self.tag2 = Tag.objects.create(
            name='shirt',
            slug='shirt',
            is_active=False,
        )
        self.brand1 = Brand.objects.create(
            name='Nike',
            slug='nike',
            is_active=True,
        )
        self.brand2 = Brand.objects.create(
            name='Adidas',
            slug='adidas',
            is_active=False,
        )
        self.product1 = Product.objects.create(
            name='Nike Skirt',
            slug='nike-skirt',
            description='Nike Skirt',
            category=self.category1,
            brand=self.brand1,
            is_active=True,
        )
        self.product1.tags.add(self.tag1)
        self.product2 = Product.objects.create(
            name='Adidas Shirt',
            slug='Adidas-Shirt',
            description='Adidas Shirt',
            category=self.category2,
            brand=self.brand2,
            is_active=False,
        )
        self.product2.tags.add(self.tag2)
        self.product_image1 = ProductImage.objects.create(
            product=self.product1,
            alt_text='Nike Skirt',
            is_active=True,
        )
        self.product_image2 = ProductImage.objects.create(
            product=self.product2,
            alt_text='Adidas Shirt',
            is_active=False,
        )
        self.product_attribute1 = ProductAttribute.objects.create(
            name='color',
            description='color'
        )
        self.product_attribute2 = ProductAttribute.objects.create(
            name='women clothing size',
            description='women clothing size'
        )
        self.product_type1 = ProductType.objects.create(
            name='women clothes',
            slug='women-clothes',
            description='women clothes'
        )
        self.product_type1.product_type_attributes.add(
            self.product_attribute1
        )
        self.product_type2 = ProductType.objects.create(
            name='men clothes',
            slug='men-clothes',
            description='men clothes'
        )
        self.product_type2.product_type_attributes.add(
            self.product_attribute2
        )
        self.product_attr_value1 = ProductAttributeValue.objects.create(
            product_attribute=self.product_attribute1,
            attribute_value='red'
        )
        self.product_attr_value2 = ProductAttributeValue.objects.create(
            product_attribute=self.product_attribute2,
            attribute_value='xs'
        )
        self.product_inventory1 = ProductInventory.objects.create(
            sku='11111',
            upc='11111',
            product=self.product1,
            product_type=self.product_type1,
            retail_price=10.00,
            store_price=11.00,
            sale_price=9.00,
            weight=float(1.0),
            is_active=True,
        )
        product_attr_value1 = ProductAttributeValue.objects.get(id=1)
        product_attr_value2 = ProductAttributeValue.objects.get(id=2)
        self.product_inventory1.attribute_values.set(
            [product_attr_value1, product_attr_value2],
        )
        self.product_inventory2 = ProductInventory.objects.create(
            sku='22222',
            upc='22222',
            product=self.product2,
            product_type=self.product_type1,
            retail_price=10.00,
            store_price=11.00,
            sale_price=9.00,
            weight=float(1.0),
            is_active=False,
        )
        self.product_inventory2.attribute_values.set(
            [product_attr_value1],
        )

    def test_category_form_has_fields(self):
        """Test the category form has the correct fields."""
        form = CategoryForm()
        expected = ['name', 'is_active']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_category_form_is_valid(self):
        """Test the category form is valid."""
        form = CategoryForm(
            data={
                'name': 'Test Category',
                'is_active': True
            }
        )
        self.assertTrue(form.is_valid())

    def test_category_form_is_invalid(self):
        """Test the category form is invalid."""
        form = CategoryForm(
            data={
                'name': '',
                'slug': 'fd',
                'is_active': True
            }
        )
        self.assertFalse(form.is_valid())

    def test_tag_form_has_fields(self):
        """Test the tag form has the correct fields."""
        form = TagForm()
        expected = ['name', 'is_active']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_tag_form_is_valid(self):
        """Test the tag form is valid."""
        form = TagForm(
            data={
                'name': 'Test Tag',
                'is_active': True
            }
        )
        self.assertTrue(form.is_valid())

    def test_tag_form_is_invalid(self):
        """Test the tag form is invalid."""
        form = TagForm(
            data={
                'name': '',
                'is_active': True
            }
        )
        self.assertFalse(form.is_valid())

    def test_brand_form_has_fields(self):
        """Test the brand form has the correct fields."""
        form = BrandForm()
        expected = ['name', 'description', 'is_active']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_brand_form_is_valid(self):
        """Test the brand form is valid."""
        form = BrandForm(
            data={
                'name': 'Test Brand',
                'description': 'Test Brand Description',
                'is_active': True
            }
        )
        self.assertTrue(form.is_valid())

    def test_brand_form_is_invalid(self):
        """Test the brand form is invalid."""
        form = BrandForm(
            data={
                'name': '',
                'description': 'Test Brand Description',
                'is_active': True
            }
        )
        self.assertFalse(form.is_valid())

    def test_product_form_has_fields(self):
        """Test the product form has the correct fields."""
        form = ProductForm()
        expected = [
            'name',
            'description',
            'category',
            'tags',
            'brand',
            'is_active'
        ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_product_form_is_valid(self):
        """Test the product form is valid."""
        form = ProductForm(
            data={
                'name': 'Test Product',
                'description': 'Test Product Description',
                'category': self.category1.id,
                'tags': [self.tag1.id],
                'brand': self.brand1.id,
                'is_active': True
            }
        )
        self.assertTrue(form.is_valid())

    def test_product_form_is_invalid(self):
        """Test the product form is invalid."""
        form = ProductForm(
            data={
                'name': 'Test Product',
                'slug': '',
                'description': 'Test Product Description',
                'category': self.category1,
                'tags': self.tag1,
                'brand': self.brand1,
                'is_active': True
            }
        )
        self.assertFalse(form.is_valid())

    def test_product_image_form_has_fields(self):
        """Test the product image form has the correct fields."""
        form = ProductImageForm()
        expected = ['product', 'image', 'alt_text', 'is_active']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_product_image_form_is_valid(self):
        """Test the product image form is valid."""
        form = ProductImageForm(
            data={
                'product': self.product1.id,
                'image': '',
                'alt_text': 'Test Alt Text',
                'is_active': True
            }
        )
        self.assertTrue(form.is_valid())

    def test_product_image_form_is_invalid(self):
        """Test the product image form is invalid."""
        form = ProductImageForm(
            data={
                'product': '',
                'image': self.product_image1.id,
                'alt_text': '',
                'is_active': True
            }
        )
        self.assertFalse(form.is_valid())

    def test_product_attribute_form_has_fields(self):
        """Test the product attribute form has the correct fields."""
        form = ProductAttributeForm()
        expected = ['name', 'description']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_product_attribute_form_is_valid(self):
        """Test the product attribute form is valid."""
        form = ProductAttributeForm(
            data={
                'name': 'Test Attribute',
                'description': 'Test Attribute Description',
            }
        )
        self.assertTrue(form.is_valid())

    def test_product_attribute_form_is_invalid(self):
        """Test the product attribute form is invalid."""
        form = ProductAttributeForm(
            data={
                'name': '',
                'description': '',
            }
        )
        self.assertFalse(form.is_valid())

    def test_product_type_form_has_fields(self):
        """Test the product type form has the correct fields."""
        form = ProductTypeForm()
        expected = [
            'name',
            'product_type_attributes',
            'description',
        ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_product_type_form_is_valid(self):
        """Test the product type form is valid."""
        form = ProductTypeForm(
            data={
                'name': 'Test Product Type',
                'product_type_attributes': [self.product_attribute1.id],
                'description': 'Test Product Type Description',
            }
        )
        self.assertTrue(form.is_valid())

    def test_product_type_form_is_invalid(self):
        """Test the product type form is invalid."""
        form = ProductTypeForm(
            data={
                'name': '',
                'product_type_attributes': self.product_attribute1.id,
                'description': '',
            }
        )
        self.assertFalse(form.is_valid())

    def test_product_attribute_value_form_has_fields(self):
        """Test the product attribute value form has the correct fields."""
        form = ProductAttributeValueForm()
        expected = ['product_attribute', 'attribute_value']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_product_attribute_value_form_is_valid(self):
        """Test the product attribute value form is valid."""
        form = ProductAttributeValueForm(
            data={
                'product_attribute': self.product_attribute1.id,
                'attribute_value': 'blue',
            }
        )
        self.assertTrue(form.is_valid())

    def test_product_attribute_value_form_is_invalid(self):
        """Test the product attribute value form is invalid."""
        form = ProductAttributeValueForm(
            data={
                'product_attribute': '',
                'attribute_value': 'green',
            }
        )
        self.assertFalse(form.is_valid())

    def test_product_inventory_form_has_fields(self):
        """Test the product inventory form has the correct fields."""
        form = ProductInventoryForm()
        expected = [
            'sku',
            'upc',
            'product',
            'product_type',
            'attribute_values',
            'retail_price',
            'store_price',
            'sale_price',
            'weight',
            'is_active',
        ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_product_inventory_form_is_valid(self):
        """Test the product inventory form is valid."""
        form = ProductInventoryForm(
            data={
                'sku': '1111111',
                'upc': '1111111',
                'product': self.product1.id,
                'product_type': self.product_type1.id,
                'attribute_values': [self.product_attr_value1.id],
                'retail_price': float('10.00'),
                'store_price': float('10.00'),
                'sale_price': float('10.00'),
                'weight': float('10.00'),
                'is_active': True,
            }
        )
        self.assertTrue(form.is_valid())

    def test_product_inventory_form_is_invalid(self):
        """Test the product inventory form is invalid."""
        form = ProductInventoryForm(
            data={
                'sku': '',
                'upc': '',
                'product': '',
                'product_type': '',
                'attribute_values': '',
                'retail_price': '',
                'store_price': '',
                'sale_price': '',
                'weight': '',
                'is_active': True,
            }
        )
        self.assertFalse(form.is_valid())

    def test_stock_form_has_fields(self):
        """Test the stock form has the correct fields."""
        form = StockForm()
        expected = [
            'last_checked',
            'units_variable',
            'units',
            'units_sold',
        ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_stock_form_is_valid(self):
        """Test the stock form is valid."""
        form = StockForm(
            data={
                'product_inventory': self.product_inventory1.id,
                'last_checked': '2020-01-01',
                'units_variable': 50,
                'units': 40,
                'units_sold': 10,
            }
        )
        self.assertTrue(form.is_valid())

    def test_stock_form_is_invalid(self):
        """Test the stock form is invalid."""
        form = StockForm(
            data={
                'product_inventory': '',
                'last_checked': '',
                'units_variable': '',
                'units': '',
                'units_sold': '',
            }
        )
        self.assertFalse(form.is_valid())
