"""Test wishlist views."""
from django.test import TestCase, Client
from django.urls import reverse
from inventory.models import (
    Category,
    Tag,
    Brand,
    Product,
)
from profiles.models import Role, User
from wishlist.models import Wishlist


class WishlistTestCase(TestCase):
    """Test case for the Wishlist model."""
    def setUp(self):
        """Set up the test case."""
        self.role1 = Role.objects.create(
            name='Customer',
            description='Customer'
        )
        self.role2 = Role.objects.create(
            name='Manager',
            description='Manager'
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
        self.client = Client()
        self.wishlist_display_url = reverse(
            'wishlist_display',
        )
        self.add_remove_product_wishlist_ajax_url = reverse(
            'add_remove_product_wishlist_ajax',
        )
        self.empty_wishlist_url = reverse(
            'empty_wishlist_ajax',
        )

    def test_wishlist_display_view(self):
        """Test wishlist display view."""
        self.client.force_login(self.user)
        response = self.client.get(self.wishlist_display_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'wishlist/wishlist_display.html',
        )
        # get wishlist of self.user
        wishlist = Wishlist.objects.get(user=self.user)
        self.assertEqual(
            wishlist.products.count(),
            0,
        )
        # add product to wishlist
        self.client.post(
            self.add_remove_product_wishlist_ajax_url,
            {
                'product_id': self.product1.id,
                'action': 'add',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        response = self.client.get(self.wishlist_display_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'wishlist/wishlist_display.html',
        )
        # check the wishlist is not empty
        wishlist = Wishlist.objects.get(user=self.user)
        self.assertEqual(
            wishlist.products.count(),
            1,
        )
        self.client.logout()
        response = self.client.get(self.wishlist_display_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_remove_product_wishlist_ajax_view(self):
        """Test add remove product wishlist ajax view."""
        self.client.force_login(self.user)
        # add product to wishlist
        response = self.client.post(
            self.add_remove_product_wishlist_ajax_url,
            {
                'product_id': self.product1.id,
                'action': 'add',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(
            response.json()['message_alert'],
            'Nike Skirt added to wishlist.',
        )
        # remove product from wishlist
        response = self.client.post(
            self.add_remove_product_wishlist_ajax_url,
            {
                'product_id': self.product1.id,
                'action': 'remove',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(
            response.json()['message_alert'],
            'Nike Skirt removed from wishlist.',
        )

    def test_add_remove_product_wishlist_ajax_view_failed(self):
        """Test add remove product wishlist ajax view failed."""
        self.client.force_login(self.user)
        # add product to wishlist
        response = self.client.post(
            self.add_remove_product_wishlist_ajax_url,
            {
                'product_id': self.product1.id,
                'action': 'add',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(
            response.json()['message_alert'],
            'Not a valid request.',
        )
        # remove product from wishlist
        response = self.client.post(
            self.add_remove_product_wishlist_ajax_url,
            {
                'product_id': self.product1.id,
                'action': 'remove',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(
            response.json()['message_alert'],
            'Not a valid request.',
        )

    def test_add_remove_product_wishlist_ajax_view_user_logout(self):
        """Test add remove product wishlist ajax view user logout."""
        # add product to wishlist
        response = self.client.post(
            self.add_remove_product_wishlist_ajax_url,
            {
                'product_id': self.product1.id,
                'action': 'add',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(
            response.json()['message_alert'],
            'You must be logged in to add to wishlist.',
        )
        self.client.logout()
        # remove product from wishlist
        response = self.client.post(
            self.add_remove_product_wishlist_ajax_url,
            {
                'product_id': self.product1.id,
                'action': 'remove',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(
            response.json()['message_alert'],
            'You must be logged in to add to wishlist.',
        )

    def test_empty_wishlist_ajax_view(self):
        """Test empty wishlist ajax view."""
        self.client.force_login(self.user)
        # add product to wishlist
        self.client.post(
            self.add_remove_product_wishlist_ajax_url,
            {
                'product_id': self.product1.id,
                'action': 'add',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        response = self.client.post(
            self.empty_wishlist_url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(
            response.json()['message_alert'],
            'Wishlist is now empty.',
        )
        # check the wishlist is empty
        response = self.client.get(self.wishlist_display_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'wishlist/wishlist_display.html',
        )
        response = self.client.get(self.wishlist_display_url + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'wishlist/wishlist_display.html',
        )
        wishlist = Wishlist.objects.get(user=self.user)
        self.assertEqual(
            wishlist.products.count(),
            0,
        )

        self.client.logout()
        response = self.client.get(self.wishlist_display_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_empty_wishlist_ajax_view_failed(self):
        """Test empty wishlist ajax view failed."""
        self.client.force_login(self.user)
        # add product to wishlist
        self.client.post(
            self.add_remove_product_wishlist_ajax_url,
            {
                'product_id': self.product1.id,
                'action': 'add',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        response = self.client.post(
            self.empty_wishlist_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(
            response.json()['message_alert'],
            'Something went wrong.',
        )
        # check the wishlist is not empty
        response = self.client.get(self.wishlist_display_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'wishlist/wishlist_display.html',
        )
        self.client.logout()
        response = self.client.get(self.wishlist_display_url + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_empty_wishlist_ajax_view_user_logout(self):
        """Test empty wishlist ajax view user logout."""
        # add product to wishlist
        self.client.post(
            self.add_remove_product_wishlist_ajax_url,
            {
                'product_id': self.product1.id,
                'action': 'add',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        response = self.client.post(
            self.empty_wishlist_url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(
            response.json()['message_alert'],
            'You must be logged in to empty wishlist.',
        )
        self.client.logout()
        response = self.client.get(self.wishlist_display_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
