"""Tests Orders views."""
from decimal import Decimal
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
from reviews.models import Review, ReviewImage


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
        self.role4 = Role.objects.create(
            name='Logistic manager',
            description='Logistic manager'
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
        self.user4 = User.objects.create_user(
            username='testuser4',
            password='Password987',
            email='logistic@gmail.com'
        )
        self.profile1 = Profile.objects.get(id=self.user.profile.id)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        self.profile4 = Profile.objects.get(id=self.user4.profile.id)
        self.profile4.role = self.role4
        self.profile4.save()
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
        self.order1_num = self.order1.order_number
        # change order1_num to F78F78B9B3DF4F7886F22F38DF241FB2
        self.order1.order_number = 'F78F78B9B3DF4F7886F22F38DF241FB2'
        self.order1.save()
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
        self.my_orders_url = reverse('my_orders', kwargs={'user': self.user})
        self.my_order_details_url = reverse(
            'my_order_details',
            kwargs={
                'user': self.user,
                'order_number': 'F78F78B9B3DF4F7886F22F38DF241FB2'
            }
        )
        self.order_details_url = reverse(
            'order_details',
            kwargs={'order_id': self.order1.id}
        )
        self.update_order_status_url = reverse('update_order_status')
        self.edit_order_url = reverse(
            'edit',
            kwargs={'order_id': self.order1.id}
        )
        self.delete_order_url = reverse(
            'delete',
            kwargs={'order_id': self.order1.id}
        )
        self.order_item1 = OrderItem.objects.create(
            order=self.order1,
            product_inventory=self.product_inventory1,
            quantity=1,
        )
        self.edit_order_item_url = reverse(
            'edit_order_item',
            kwargs={'order_item_id': self.order_item1}
        )
        self.delete_order_item_url = reverse(
            'delete_order_item',
            kwargs={'order_item_id': self.order_item1}
        )

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

    def test_orders_view_search_query(self):
        """Test orders view search query"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.order_url,
            {'search_query': 'F78F78B9B3DF4F7886F22F38DF241FB2'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/orders.html')
        self.assertEqual(len(response.context['orders']), 1)
        self.assertEqual(
            response.context['orders'][0].order_number,
            'F78F78B9B3DF4F7886F22F38DF241FB2'
        )

    def test_orders_view_search_query_no_results(self):
        """Test orders view search query no results"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.order_url, {'search_query': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/orders.html')
        self.assertEqual(len(response.context['orders']), 1)

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
        self.assertEqual(OrderItem.objects.count(), 2)
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

    def test_my_orders_view_user_logged_out(self):
        """Test my orders view user logged out"""
        response = self.client.get(self.my_orders_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_my_orders_view_user_logged_in(self):
        """Test my orders view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(self.my_orders_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/user_orders.html')

    def test_my_order_details_view_user_logged_logged_out(self):
        """Test my orders view user logged out"""
        response = self.client.get(self.my_order_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_my_order_details_view_user_logged_logged_in(self):
        """Test my orders view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(self.my_order_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/user_order_details.html')

    def test_if_product_in_order_has_review(self):
        """Test if product in order has review"""
        self.client.force_login(self.user)
        # create review
        self.review1 = Review.objects.create(
            user=self.user,
            product=self.product1,
            order=self.order1,
            rating=5,
            comment='Good product',
        )
        # create review image
        self.review_image1 = ReviewImage.objects.create(
            review=self.review1,
            image='',
        )
        bag = self.client.session['bag']
        self.assertEqual(bag['1'], 1)
        self.assertEqual(Order.objects.count(), 1)
        response = self.client.get(self.my_order_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/user_order_details.html')
        self.assertEqual(
            response.context['products_in_reviews'],
            [self.product1]
        )

    def test_my_order_details_view_user_logged_logged_in_not_user(self):
        """Test my orders view OTHER user logged in"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.my_order_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_order_details_view_user_logged_out(self):
        """Test my orders view user logged in"""
        response = self.client.get(self.order_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_order_details_view_user_logged_logged_in_without_access(self):
        """Test my orders view OTHER user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(self.order_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_order_details_view_user_logged_with_access(self):
        """Test my orders view user logged in"""
        self.client.force_login(self.user2)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.order_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_details.html')

    def test_update_order_status_ajax_view_user_logged_out(self):
        """Test update order status ajax view user logged out"""
        response = self.client.post(
            self.update_order_status_url,
            data={
                'order_id': self.order1.id,
                'order_status': 'Completed',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_update_order_status_ajax_view_user_logged_customer(self):
        """Test update order status ajax view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.update_order_status_url,
            data={
                'order_id': self.order1.id,
                'order_status': 'Completed',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_update_order_status_ajax_view_staff_logged_without_access(self):
        """Test update order status ajax view user logged in with access"""
        self.client.force_login(self.user2)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.update_order_status_url,
            data={
                'order_id': self.order1.id,
                'order_status': 'Completed',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_update_order_status_ajax_view_admin_logged_with_access(self):
        """Test update order status ajax view user logged in with access"""
        self.client.force_login(self.user3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        self.assertEqual(self.order1.status, 'Pending')
        response = self.client.post(
            self.update_order_status_url,
            data={
                'order_id': self.order1.id,
                'order_status': 'Completed',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        # check if order status was updated
        self.order1 = Order.objects.get(id=self.order1.id)
        self.assertEqual(self.order1.status, 'Completed')

    def test_update_order_status_ajax_view_logistic_manager_with_access(self):
        """Test update order status ajax view user logged in with access"""
        self.client.force_login(self.user4)
        self.profile4 = Profile.objects.get(id=self.user4.profile.id)
        self.profile4.role = self.role4
        self.profile4.save()
        self.assertEqual(self.order1.status, 'Pending')
        response = self.client.post(
            self.update_order_status_url,
            data={
                'order_id': self.order1.id,
                'order_status': 'Completed',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        # check if order status was updated
        self.order1 = Order.objects.get(id=self.order1.id)
        self.assertEqual(self.order1.status, 'Completed')

    def test_update_order_status_ajax_view_with_access_failed(self):
        """Test update order status ajax view user logged in with access"""
        self.client.force_login(self.user4)
        self.profile4 = Profile.objects.get(id=self.user4.profile.id)
        self.profile4.role = self.role4
        self.profile4.save()
        self.assertEqual(self.order1.status, 'Pending')
        response = self.client.post(
            self.update_order_status_url,
            data={
                'order_id': self.order1.id,
                'order_status': 'Completed',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        # check if order status was updated
        self.order1 = Order.objects.get(id=self.order1.id)
        self.assertEqual(self.order1.status, 'Pending')

    def test_edit_order_get_view_user_logged_out(self):
        """Test edit order get view user logged out"""
        response = self.client.get(self.edit_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_order_get_view_user_logged_customer(self):
        """Test edit order get view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(self.edit_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_edit_order_get_view_user_logged_staff_without_access(self):
        """Test edit order get view user logged in with access"""
        self.client.force_login(self.user2)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.edit_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_edit_order_get_view_user_logged_admin_with_access(self):
        """Test edit order get view user logged in with access"""
        self.client.force_login(self.user3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(self.edit_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/edit_order.html')

    def test_edit_order_post_view_user_logged_out(self):
        """Test edit order post view user logged out"""
        response = self.client.post(self.edit_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_order_post_view_user_logged_customer(self):
        """Test edit order post view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.post(self.edit_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_edit_order_post_view_user_logged_staff_without_access(self):
        """Test edit order post view user logged in with access"""
        self.client.force_login(self.user2)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(self.edit_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_edit_order_post_view_user_logged_admin_with_access_invalid(self):
        """Test edit order post view user logged in with access"""
        self.client.force_login(self.user3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.post(
            self.edit_order_url,
            data={
                'order_id': self.order1.id,
                'order_status': 'Completed',
                'order_total': '100',
                'order_date': '2020-01-01',
                'order_customer': self.user3.id,
                'order_staff': self.user3.id,
                'order_products': [self.product1.id, self.product2.id],
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/edit_order.html')

    def test_edit_order_post_view_user_logged_admin_with_access_valid(self):
        """Test edit order post view user logged in with access"""
        self.client.force_login(self.user3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        # check status of the order before update
        self.assertEqual(self.order1.status, 'Pending')
        response = self.client.post(
            self.edit_order_url,
            data={
                'order_id': self.order1.id,
                'full_name': 'Test User',
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
            },
        )
        self.assertEqual(response.status_code, 302)
        # check if order status was updated
        self.order1 = Order.objects.get(id=self.order1.id)
        self.assertEqual(self.order1.status, 'Completed')

    def test_delete_order_get_view_user_logged_out(self):
        """Test delete order get view user logged out"""
        response = self.client.get(self.delete_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_order_get_view_user_logged_customer(self):
        """Test delete order get view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(self.delete_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_delete_order_get_view_user_logged_staff_without_access(self):
        """Test delete order get view user logged in with access"""
        self.client.force_login(self.user2)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.delete_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_delete_order_get_view_user_logged_admin_with_access(self):
        """Test delete order get view user logged in with access"""
        self.client.force_login(self.user3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(self.delete_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/delete_order.html')

    def test_delete_order_post_view_user_logged_out(self):
        """Test delete order post view user logged out"""
        response = self.client.post(self.delete_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_order_post_view_user_logged_customer(self):
        """Test delete order post view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.post(self.delete_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_delete_order_post_view_user_logged_staff_without_access(self):
        """Test delete order post view user logged in with access"""
        self.client.force_login(self.user2)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(self.delete_order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_delete_order_post_view_user_logged_admin_with_access(self):
        """Test delete order post view user logged in with access"""
        self.client.force_login(self.user3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.post(self.delete_order_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/orders/')
        # check if order was deleted
        self.assertEqual(Order.objects.filter(id=self.order1.id).count(), 0)

    def test_edit_order_item_get_view_user_logged_out(self):
        """Test edit order item get view user logged out"""
        response = self.client.get(self.edit_order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_order_item_get_view_user_logged_customer(self):
        """Test edit order item get view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(self.edit_order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_edit_order_item_get_view_user_logged_staff_without_access(self):
        """Test edit order item get view user logged in with access"""
        self.client.force_login(self.user2)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.edit_order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_edit_order_item_get_view_user_logged_admin_with_access(self):
        """Test edit order item get view user logged in with access"""
        self.client.force_login(self.user3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(self.edit_order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/edit_order_item.html')

    def test_edit_order_item_post_view_user_logged_out(self):
        """Test edit order item post view user logged out"""
        response = self.client.post(self.edit_order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_order_item_post_view_user_logged_customer(self):
        """Test edit order item post view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.post(self.edit_order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_edit_order_item_post_view_user_logged_staff_without_access(self):
        """Test edit order item post view user logged in with access"""
        self.client.force_login(self.user2)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(self.edit_order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_edit_order_item_post_view_admin_with_access_failed(self):
        """Test edit order item post view user logged in with access"""
        self.client.force_login(self.user3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.post(
            self.edit_order_item_url,
            data={
                'quantity': '2',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/edit_order_item.html')

    def test_edit_order_item_post_view_admin_with_access_valid_form(self):
        """Test edit order item post view user logged in with access"""
        self.client.force_login(self.user3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        self.assertEqual(
            OrderItem.objects.get(id=self.order_item1.id).quantity,
            1
        )
        self.assertEqual(
            Order.objects.get(id=self.order1.id).total_paid,
            Decimal('10.00')
        )
        response = self.client.post(
            self.edit_order_item_url,
            {
              'order': self.order1.id,
              'product_inventory': self.product_inventory1.id,
              'quantity': '2',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/orders/order_details/1')
        # check if order item was updated
        self.assertEqual(
            OrderItem.objects.get(id=self.order_item1.id).quantity,
            2
        )
        # check if order was updated
        self.assertEqual(
            Order.objects.get(id=self.order1.id).total_paid,
            Decimal('19.00')
        )

    def test_delete_order_item_get_view_user_logged_out(self):
        """Test delete order item get view user logged out"""
        response = self.client.get(self.delete_order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_order_item_get_view_user_logged_customer(self):
        """Test delete order item get view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(self.delete_order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_delete_order_item_get_view_staff_without_access(self):
        """Test delete order item get view user logged in with access"""
        self.client.force_login(self.user2)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.delete_order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_delete_order_item_get_view_admin_with_access(self):
        """Test delete order item get view user logged in with access"""
        self.client.force_login(self.user3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(self.delete_order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/delete_order_item.html')

    def test_delete_order_item_post_view_user_logged_out(self):
        """Test delete order item post view user logged out"""
        response = self.client.post(self.delete_order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_order_item_post_view_user_logged_customer(self):
        """Test delete order item post view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.post(self.delete_order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_delete_order_item_post_view_staff_without_access(self):
        """Test delete order item post view user logged in with access"""
        self.client.force_login(self.user2)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(self.delete_order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')

    def test_delete_order_item_post_view_admin_with_access(self):
        """Test delete order item post view user logged in with access"""
        self.client.force_login(self.user3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.post(self.delete_order_item_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/orders/order_details/1')
        # check if order item was deleted
        self.assertEqual(
            OrderItem.objects.filter(id=self.order_item1.id).count(),
            0
        )
        # check if order was updated
        self.assertEqual(
            Order.objects.get(id=self.order1.id).total_paid,
            Decimal('1.00')
        )
