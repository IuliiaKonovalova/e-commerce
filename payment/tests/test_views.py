"""Test Payment Views."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import Role, Profile, Address
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
    Stock,
)


class TestPaymentViews(TestCase):
    """Test Payment Views."""

    def setUp(self):
        """Set up."""
        # create user
        self.role1 = Role.objects.create(
            name='Customer',
            description='Customer'
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='Password987',
            email='testuser@gmail.com'
        )
        self.address1 = Address.objects.create(
            user=self.user,
            country='USA',
            county_region='California',
            city='San Francisco',
            address_line='123 Main St',
            zip_code='12345',
            phone_number='1234567890',
            is_primary=True,
            created_at='2020-01-01',
            updated_at='2020-01-01'
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
        # create stock
        self.stock = Stock.objects.create(
            product_inventory=self.product_inventory1,
            units_variable=10,
            units=10,
            units_sold=0,
        )
        self.client = Client()
        # urls
        self.add_to_bag_url = reverse('add_to_bag')
        bag_items = []
        total = 0
        product_item_total = 0
        response = self.client.post(
            self.add_to_bag_url,
            {'product_inventory_id': 1, 'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertTrue(self.client.session['bag'], {})
        # get data from the bag
        bag = self.client.session['bag']
        # check that it isinstance of dict: if isinstance(item_data, int):
        self.assertTrue(isinstance(bag, dict))
        # get product inventory by product_inventory_id from the dict
        product_inventory = ProductInventory.objects.get(id=bag['1'])
        # check that product_inventory is not None
        self.assertIsNotNone(product_inventory)
        #  check the quantity of the product
        self.assertEqual(bag['1'], 1)
        # check the product_item_total
        product_item_total = product_inventory.sale_price * bag['1']
        # count the total
        total = product_inventory.sale_price * bag['1']
        # add product_inventory_id, quantity, product_item_total,
        # total to bag_items
        bag_items.append({
            'product_inventory': product_inventory,
            'product_item_total': product_item_total,
            'quantity': bag['1'],
        })
        self.payment_url = reverse('payment')
        self.order_placed_url = reverse('order_placed')

    def test_payment_view(self):
        """Test payment view."""
        # login
        self.client.force_login(self.user)
        # get payment view
        response = self.client.get(self.payment_url)
        # check status code
        self.assertEqual(response.status_code, 200)
        # check template
        self.assertTemplateUsed(response, 'payment/payment.html')
        # check context
        self.assertTrue('primary_address' in response.context)
        self.assertTrue('total_sum' in response.context)
        self.assertTrue('client_secret' in response.context)
        self.assertTrue('stripe_public_key' in response.context)

    def test_order_placed_view(self):
        """Test order placed view."""
        # login
        self.client.force_login(self.user)
        # check how many units are in the stock
        # get bag
        bag = self.client.session['bag']
        # check how many units are in the bag
        self.assertEqual(bag['1'], 1)
        # get product inventory by product_inventory_id from the dict
        product_inventory = ProductInventory.objects.get(id=bag['1'])
        # check how many units are in the stock
        self.assertEqual(product_inventory.stock.units, 10)
        self.assertEqual(self.stock.units, 10)
        # check how many sold_units are in the stock
        self.assertEqual(self.stock.units_sold, 0)
        response = self.client.post(self.order_placed_url)
        self.assertTemplateUsed(response, 'payment/order_placed.html')
        self.assertEqual(response.status_code, 200)
