"""Tests email_notifications views."""
from django.test import TestCase, Client
from django.urls import reverse
import json
from django.contrib.auth.models import User
from profiles.models import Role, Profile
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
from email_notifications.models import StockEmailNotification


class EmailStockNotificationFormAJAXTest(TestCase):
    """Tests for the email stock notification form AJAX."""

    def setUp(self):
        """Set up the test."""
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
        # create product_inventories + stock
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
        self.product_attr_value11 = ProductAttributeValue.objects.create(
            product_attribute=self.product_attribute1,
            attribute_value='blue'
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
        self.product_inventory11 = ProductInventory.objects.create(
            sku='11112',
            upc='11112',
            product=self.product1,
            product_type=self.product_type1,
            retail_price=10.00,
            store_price=11.00,
            sale_price=9.00,
            weight=float(1.0),
            is_active=True,
        )
        product_attr_value11 = ProductAttributeValue.objects.get(id=3)
        product_attr_value2 = ProductAttributeValue.objects.get(id=2)
        self.product_inventory11.attribute_values.set(
            [product_attr_value11, product_attr_value2],
        )

        # create stock
        self.stock = Stock.objects.create(
            product_inventory=self.product_inventory1,
            units_variable=10,
            units=10,
            units_sold=0,
        )
        # set Client
        self.client = Client()

        # add url
        self.stock_notification_url = reverse(
            'add_to_stock_email_notification'
        )
        self.add_promo_email_url = reverse(
            'add_promo_email'
        )
        self.stock_requests_list_url = reverse(
            'stock_requests_list'
        )

    def test_email_stock_notification_form_ajax_user_logged_out(self):
        """Test email stock notification form AJAX user logged out."""
        data_initail = {
            'id': 1,
            'options': {
                'Color': 'red',
                'women clothes': 'xs',
            },
            'quantity': '1',
        }
        response = self.client.post(
            self.stock_notification_url,
            data=data_initail,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_email_stock_notification_form_ajax_user_logged_in(self):
        """Test email stock notification form AJAX user logged in."""
        self.client.force_login(self.user)
        data = (
            '{"id":2,"options": ' +
            '{"color":"red","women clothing size":"xs"}, ' +
            '"quantity":"1"}'
        )
        response = self.client.post(
            self.stock_notification_url,
            data={
              'data': data
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

    def test_email_stock_notification_form_ajax_failed(self):
        """Test email stock notification form AJAX user logged in."""
        self.client.force_login(self.user)
        data = (
            '{"id":2,"options": ' +
            '{"color":"red","women clothing size":"xs"}, ' +
            '"quantity":"1"}'
        )
        response = self.client.post(
            self.stock_notification_url,
            data={
              'data': data
            },
        )
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

    def test_email_stock_notification_form_ajax_user_got_target(self):
        """Test email stock notification response for getting sku"""
        self.client.force_login(self.user)
        data = (
            '{"id":2,"options": ' +
            '{"color":"red","women clothing size":"xs"}, ' +
            '"quantity":"1"}'
        )
        response = self.client.post(
            self.stock_notification_url,
            data={
              'data': data
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

    def test_promo_email_create_get_view_user_logged_out(self):
        """Test promo email create post view user logged out."""
        response = self.client.get(self.add_promo_email_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_promo_email_create_get_view_user_logged_no_access(self):
        """Test promo email create post view user logged no access."""
        self.client.force_login(self.user)
        # check a role
        self.assertEqual(self.user.profile.role.id, 1)
        response = self.client.get(self.add_promo_email_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_promo_email_create_get_view_user_logged_with_access(self):
        """Test promo email create post view user logged with access."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.add_promo_email_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'email_notifications/promo_email_create.html'
        )
        self.client.logout()

    def test_promo_email_create_post_view_user_logged_out(self):
        """Test promo email create post view user logged out."""
        response = self.client.post(self.add_promo_email_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_promo_email_create_post_view_user_logged_no_access(self):
        """Test promo email create post view user logged no access."""
        self.client.force_login(self.user)
        # check a role
        self.assertEqual(self.user.profile.role.id, 1)
        response = self.client.post(self.add_promo_email_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_promo_email_create_post_view_user_logged_with_access(self):
        """Test promo email create post view user logged with access."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.add_promo_email_url,
            data={
                'email_name': 'test',
                'content': 'test',
            }

        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'promotions/promotions_list.html')
        self.client.logout()

    def test_promo_email_create_post_view_user_with_access_failed(self):
        """
        Test promo email create post view user logged
        with access but failed to fill out the form.
        """
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.add_promo_email_url,
            data={
                'email_name': '',
                'content': 'test',
            }

        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'email_notifications/promo_email_create.html'
        )
        self.client.logout()

    def test_stock_requests_list_view_user_logged_out(self):
        """Test stock requests list view user logged out."""
        response = self.client.get(self.stock_requests_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_stock_requests_list_view_user_logged_no_access(self):
        """Test stock requests list view user logged no access."""
        self.client.force_login(self.user)
        # check a role
        self.assertEqual(self.user.profile.role.id, 1)
        response = self.client.get(self.stock_requests_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_stock_requests_list_view_user_logged_with_access(self):
        """Test stock requests list view user logged with access."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.stock_requests_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'email_notifications/stock_requests_list.html'
        )
        self.client.logout()

    def test_stock_requests_list_view_staff_search_query(self):
        """Test stock requests list view staff search query."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        data = (
            '{"id":2,"options": ' +
            '{"color":"red","women clothing size":"xs"}, ' +
            '"quantity":"1"}'
        )
        response = self.client.post(
            self.stock_notification_url,
            data={
              'data': data
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        response = self.client.get(
            self.stock_requests_list_url,
            data={
                'search_query': 'Adidas Shirt',
            }
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'email_notifications/stock_requests_list.html'
        )
        self.assertEqual(len(response.context['stock_requests']), 1)
        self.client.logout()

    def test_stock_requests_list_view_staff_search_query_empty(self):
        """Test stock requests list view staff search query empty."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        data = (
            '{"id":2,"options": ' +
            '{"color":"red","women clothing size":"xs"}, ' +
            '"quantity":"1"}'
        )
        response = self.client.post(
            self.stock_notification_url,
            data={
              'data': data
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        response = self.client.get(
            self.stock_requests_list_url,
            data={
                'search_query': '',
            }
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'email_notifications/stock_requests_list.html'
        )
        self.assertEqual(len(response.context['stock_requests']), 1)
