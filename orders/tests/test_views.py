"""Tests Orders views."""
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
from orders.models import Order, OrderItem


class TestOrdersViews(TestCase):
    """Test Orders views."""

    def setUp(self):
        """Set up."""
        # create users
        self.role1 = Role.objects.create(
            name='Customer',
            description='Customer'
        )
        self.role2 = Role.objects.create(
            name='Manager',
            description='Manager'
        )
        self.role3 = Role.objects.create(
            name='Admin',
            description='Admin'
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='Password987',
            email='testuser@gmail.com'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='Password987',
            email='testuser2@gmail.com'
        )
        self.user3 = User.objects.create_user(
            username='testuser3',
            password='Password987',
            email='admin@gmail.com'
        )
        self.profile1 = Profile.objects.get(id=self.user.profile.id)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
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
        # urls
        self.client = Client()
        # set bag
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
        bag = self.client.session['bag']
        self.assertTrue(isinstance(bag, dict))
        product_inventory = ProductInventory.objects.get(id=bag['1'])
        self.assertIsNotNone(product_inventory)
        self.assertEqual(bag['1'], 1)
        product_item_total = product_inventory.sale_price * bag['1']
        total = product_inventory.sale_price * bag['1']
        bag_items.append({
            'product_inventory': product_inventory,
            'product_item_total': product_item_total,
            'quantity': bag['1'],
        })
        self.order_url = reverse('orders')
        self.add_url = reverse('add')

        self.add_to_bag_url = reverse('add_to_bag')

    def test_orders_view_user_logged_out(self):
        """Test orders view user logged out"""
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_orders_view_user_logged_in_without_access(self):
        """Test orders view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_orders_view_user_logged_in_with_access(self):
        """Test orders view user logged in with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/orders.html')

    def test_add_order_ajax_view_user_logged_out(self):
        """Test add order ajax view user logged out"""
        response = self.client.post(
            self.add_url,
            data={
                'full_name': ['John Doe'],
                'email': ['john@gmail.com'],
                'phone': ['123456789'],
                'address1': ['123 Main St'],
                'address2': [''],
                'country': ['US'],
                'county_region_state': ['CA'],
                'city': ['San Francisco'],
                'zip_code': ['94107'],
                'total_paid': ['10.00'],
                'order_key': ['12345sfsdfsdgsrz67terte4n89'],
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_order_ajax_view(self):
        """Test add order ajax view"""
        self.client.force_login(self.user)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        bag = self.client.session['bag']
        # check how many units are in the bag
        self.assertEqual(bag['1'], 1)
        self.assertEqual(Order.objects.count(), 1)
        response = self.client.post(
            self.add_url,
            data={
                'full_name': ['John Doe'],
                'email': ['john@gmail.com'],
                'phone': ['123456789'],
                'address1': ['123 Main St'],
                'address2': [''],
                'country': ['US'],
                'county_region_state': ['CA'],
                'city': ['San Francisco'],
                'zip_code': ['94107'],
                'total_paid': ['10.00'],
                'order_key': ['12345sfsdfsdgsrz67terte4n89'],
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(
            Order.objects.get(order_key='12345sfsdfsdgsrz67terte4n89').status,
            'Pending'
        )
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(
            OrderItem.objects.get(
                order=Order.objects.get(
                    order_key='12345sfsdfsdgsrz67terte4n89'
                )
            ).product_inventory,
            self.product_inventory1
        )

    def test_add_order_ajax_view_failed(self):
        """Test add order ajax view"""
        self.client.force_login(self.user)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.add_url,
            data={
                'full_name': ['John Doe'],
                'email': ['john@gmail.com'],
                'phone': ['123456789'],
                'address1': ['123 Main St'],
                'address2': [''],
                'country': ['US'],
                'county_region_state': ['CA'],
                'city': ['San Francisco'],
                'zip_code': ['94107'],
                'total_paid': ['10.00'],
                'order_key': ['12345sfsdfsdgsrz67terte4n89'],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)


    def test_add_order_ajax_view_order_exist(self):
        """Test add order ajax view"""
        self.client.force_login(self.user)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        bag = self.client.session['bag']
        # check how many units are in the bag
        self.assertEqual(bag['1'], 1)
        response = self.client.post(
            self.add_url,
            data={
                'full_name': ['John Doe'],
                'email': ['john@gmail.com'],
                'phone': ['123456789'],
                'address1': ['123 Main St'],
                'address2': [''],
                'country': ['US'],
                'county_region_state': ['CA'],
                'city': ['San Francisco'],
                'zip_code': ['94107'],
                'total_paid': ['10.00'],
                'order_key': ['1111111sdgsrz67terte4n89'],
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(
            Order.objects.get(order_key='1111111sdgsrz67terte4n89').status,
            'Pending'
        )
