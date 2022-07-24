"""Test forms for orders app"""
from django.test import TestCase
from django.urls import reverse
from orders.forms import OrderForm, OrderItemForm
from django.contrib.auth.models import User
from profiles.models import Role
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
from orders.models import Order


class OrderFormTest(TestCase):
    """Test case for the Order model."""
    def setUp(self):
        """Set up test data."""
        # create users
        self.role1 = Role.objects.create(
            name='Customer',
            description='Customer'
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='Password987',
            email='testuser@gmail.com'
        )
        # set Products
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
        )
        self.product2 = Product.objects.create(
            name='Adidas Shirt',
            slug='adidas-shirt',
            description='Adidas Shirt',
            category=self.category2,
            brand=self.brand2,
        )
        self.product3 = Product.objects.create(
            name='Adidas Skirt',
            slug='adidas-skirt',
            description='Adidas Skirt',
            category=self.category1,
            brand=self.brand2,
        )
        self.product4 = Product.objects.create(
            name='Nike Shirt',
            slug='nike-shirt',
            description='Nike Shirt',
            category=self.category2,
            brand=self.brand1,
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
        # set order
        self.order1 = Order.objects.create(
            user=self.user,
            full_name='John Doe',
            email='john@gmail.com',
            phone='123456789',
            address1='123 Main St',
            address2='',
            country='US',
            county_region_state='CA',
            city='San Francisco',
            zip_code=94107,
            total_paid=10.00,
            order_key='1111111sdgsrz67terte4n89',
        )

    def test_order_has_fields(self):
        """Test order form has expected fields."""
        expected = [
            'full_name',
            'email',
            'phone',
            'address1',
            'address2',
            'city',
            'county_region_state',
            'country',
            'zip_code',
            'total_paid',
            'billing_status',
            'status',
        ]
        actual = list(OrderForm().fields)
        self.assertListEqual(expected, actual)

    def test_order_form_is_valid(self):
        """Test order form is valid."""
        form = OrderForm({
            'full_name': 'Test Order',
            'email': 'test@mail.com',
            'phone': '1234567890',
            'address1': 'Test Address 1',
            'address2': 'Test Address 2',
            'city': 'Test City',
            'county_region_state': 'Test County',
            'country': 'Test Country',
            'zip_code': '12345',
            'total_paid': 10,
            'billing_status': True,
            'status': 'Completed',
        })
        self.assertTrue(form.is_valid())

    def test_order_form_is_invalid(self):
        """Test order form is invalid."""
        form = OrderForm({
            'full_name': '',
            'email': '',
            'phone': '',
            'address1': '',
            'address2': '',
            'city': '',
            'county_region_state': '',
            'country': '',
            'zip_code': '',
            'total_paid': '',
            'billing_status': '',
            'status': '',
        })
        self.assertFalse(form.is_valid())

    def test_order_item_form_has_fields(self):
        """Test order item form has expected fields."""
        expected = [
            'order',
            'product_inventory',
            'quantity',
        ]
        actual = list(OrderItemForm().fields)
        self.assertListEqual(expected, actual)

    def test_order_item_form_is_valid(self):
        """Test order item form is valid."""
        form = OrderItemForm({
            'order': self.order1.id,
            'product_inventory': self.product_inventory1.id,
            'quantity': 1,
        })
        self.assertTrue(form.is_valid())

    def test_order_item_form_is_invalid(self):
        """Test order item form is invalid."""
        form = OrderItemForm({
            'order': '',
            'product_inventory': '',
            'quantity': '',
        })
        self.assertFalse(form.is_valid())
