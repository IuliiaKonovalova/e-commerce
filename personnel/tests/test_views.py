"""Test Inventory views."""
from django.test import TestCase, Client
# import QueryDict
from django.http import QueryDict
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
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
    ProductAttributeValues,
    ProductTypeAttribute,
)
from promotions.models import Promotion


class TestViews(TestCase):
    """Test Inventory Views."""
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
        # Create promotion
        self.promotion = Promotion.objects.create(
            name='Promotion 1',
            slug='promotion-1',
            description='Promotion 1 description',
            promotion_code='PROMO1',
            promotion_reduction=10,
            start_date=datetime.now(),
            end_date=datetime.now() + timezone.timedelta(days=365 * 5),
            active=True,
        )
        # urls
        self.client = Client()
        self.products_table_url = reverse('products_table')
        self.product_detail_full_url = reverse(
            'product_detail_full',
            kwargs={'pk': 1}
        )
        self.add_product_url = reverse('add_product')
        self.edit_product_url = reverse('edit_product', kwargs={'pk': 1})
        self.delete_product_url = reverse(
            'delete_product',
            kwargs={'pk': 1,}
        )
        self.add_product_image_url = reverse('add_product_image')
        self.edit_product_image_url = reverse('edit_product_image')
        self.delete_product_image_url = reverse('delete_product_image')
        self.product_inventory_details_url = reverse(
            'product_inventory_details',
            kwargs={'pk': 1, 'inventory_pk': 1}
        )
        self.add_product_inventory_details_url = reverse(
            'add_product_inventory_details',
            kwargs={'pk': 1}
        )
        self.get_type_attribute_url = reverse(
            'get_type_attribute'
        )
        self.product_inventory_create_url = reverse(
            'product_inventory_create'
        )
        self.edit_product_inventory_url = reverse(
            'edit_product_inventory',
            kwargs={'pk': 1, 'inventory_pk': 1}
        )
        self.product_inventory_update_url = reverse(
            'product_inventory_update',
        )

    def test_products_table_view_user_logged_out(self):
        """Test products table view user logged out."""
        response = self.client.get(self.products_table_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_products_table_view_without_access(self):
        """Test products table view without access."""
        self.client.force_login(self.user)
        response = self.client.get(self.products_table_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_products_table_view_with_access(self):
        """Test products table view with access."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.products_table_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/products_table.html')

    def test_product_detail_full_view_user_logged_out(self):
        """Test product detail full view user logged out."""
        response = self.client.get(self.product_detail_full_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_product_detail_full_view_without_access(self):
        """Test product detail full view without access."""
        self.client.force_login(self.user)
        response = self.client.get(self.product_detail_full_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_product_detail_full_view_with_access(self):
        """Test product detail full view with access."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.promotion.products_inventory_in_promotion.add(
            self.product_inventory1
        )
        self.promotion.save()
        response = self.client.get(self.product_detail_full_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/product_detail_full.html'
        )
        self.assertIn(
            self.product_inventory1,
            response.context['product_inventory_in_promo_now'],
        )

    def test_add_product_view_user_logged_out(self):
        """Test add product view user logged out."""
        response = self.client.get(self.add_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_product_view_without_access(self):
        """Test add product view without access."""
        self.client.force_login(self.user)
        response = self.client.get(self.add_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_product_view_with_access(self):
        """Test add product view with access."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.add_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/add_product.html')

    def test_add_product_post_view_user_logged_out(self):
        """Test add product post view user logged out"""
        response = self.client.post(self.add_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_product_post_view_without_access(self):
        """Test add product post view without access"""
        self.client.force_login(self.user)
        response = self.client.post(self.add_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_product_post_view_with_access(self):
        """Test add product post view with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.add_product_url,
            {
                'name': 'Test Product',
                'description': 'Test Product Description',
                'category': self.category1.id,
                'tags': [self.tag1.id],
                'brand': self.brand1.id,
                'is_active': True
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_add_product_post_view_with_access_failed(self):
        """Test add product post view with access failed."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.add_product_url,
            {
                'name': 'Test Product',
                'description': 'Test Product Description',
                'brand': self.brand1.id,
                'is_active': True
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/add_product.html')

    def test_edit_product_view_user_logged_out(self):
        """Test edit product view user logged out."""
        response = self.client.get(self.edit_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_product_view_without_access(self):
        """Test edit product view without access."""
        self.client.force_login(self.user)
        response = self.client.get(self.edit_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_product_view_with_access(self):
        """Test edit product view with access."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.edit_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/edit_product.html')

    def test_edit_product_post_view_user_logged_out(self):
        """Test edit product post view user logged out"""
        response = self.client.post(self.edit_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_product_post_view_without_access(self):
        """Test edit product post view without access"""
        self.client.force_login(self.user)
        response = self.client.post(self.edit_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_product_post_view_with_access(self):
        """Test edit product post view with access."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.edit_product_url,
            {
                'name': 'Test Product',
                'description': 'Test Product Description',
                'category': self.category1.id,
                'tags': [self.tag1.id],
                'brand': self.brand1.id,
                'is_active': True
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_edit_product_post_view_with_access_failed(self):
        """Test edit product post view with access failed."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.edit_product_url,
            {
                'name': '',
                'description': 'Test Product Description',
                'brand': self.brand1.id,
                'is_active': True
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/edit_product.html')

    def test_delete_product_view_user_logged_out(self):
        """Test delete product view user logged out."""
        response = self.client.get(self.delete_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_product_view_without_access(self):
        """Test delete product view without access."""
        self.client.force_login(self.user)
        response = self.client.get(self.delete_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_product_view_with_access(self):
        """Test delete product view with access."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.delete_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/delete_product.html')

    def test_delete_product_post_view_user_logged_out(self):
        """Test delete product post view user logged out."""
        response = self.client.post(self.delete_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_product_post_view_without_access(self):
        """Test delete product post view without access."""
        self.client.force_login(self.user)
        response = self.client.post(self.delete_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_product_post_view_with_access(self):
        """Test delete product post view with access."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        # check how many products are in the database
        self.assertEqual(Product.objects.count(), 4)
        response = self.client.post(self.delete_product_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 3)

    def test_add__product_image_view_user_logged_out(self):
        """Test add product image view user logged out"""
        response = self.client.post(
            self.add_product_image_url,
            {
                'product': self.product1,
                'image': '',
                'alt_text': 'Test Image Alt Text',
                'default_image': True,
                'is_active': True
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add__product_image_view_without_access(self):
        """Test add product image view without access"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.add_product_image_url,
            {
                'product': self.product1,
                'image': '',
                'alt_text': 'Test Image Alt Text',
                'default_image': True,
                'is_active': True
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add__product_image_view_with_access(self):
        """Test add product Image view with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        product5 = Product.objects.create(
            name='Test Product 5',
            description='Test Product Description',
            category=self.category1,
            brand=self.brand1,
            is_active=True
        )
        response = self.client.post(
            self.add_product_image_url,
            {
                'product_id': 1,
                'image': '',
                'alt_text': 'Test Image Alt Text',
                'default_image': True,
                'is_active': True
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

    def test_add__product_image_view_with_access_failed(self):
        """TEST: add product image view with access failed"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        image = open('static/images/test_product_image.png', 'rb')
        response = self.client.post(
            self.add_product_image_url,
            {
                'product': '1',
                'image': image,
                'alt_text': 'Test Image Alt Text',
                'default_image': True,
                'is_active': True
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

    def test_edit_product_ajax_post_view_user_logged_out(self):
        """test edit product ajax post view user logged out"""
        response = self.client.post(self.edit_product_image_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_product_ajax_post_view_without_access(self):
        """Test edit product ajax post view without access"""
        self.client.force_login(self.user)
        response = self.client.post(self.edit_product_image_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_product_ajax_post_view_with_access(self):
        """Test edit product image ajax post view with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.edit_product_image_url,
            {
                'product_id': 1,
                'image_id': 1,
                'image': '',
                'alt_text': 'Test Edit Image Alt Text',
                'default_image': True,
                'is_active': True
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

    def test_edit_product_ajax_post_view_with_access_with_image(self):
        """Test edit product image ajax post view with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        image = open('static/images/test_product_image.png', 'rb')
        response = self.client.post(
            self.edit_product_image_url,
            {
                'product_id': 1,
                'image_id': 1,
                'image': image,
                'alt_text': 'Test Edit Image Alt Text',
                'default_image': True,
                'is_active': True
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

    def test_edit_product_ajax_post_view_with_access_failed(self):
        """Test edit product image view with access failed"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.edit_product_image_url,
            {
                'product_id': self.product1.id,
                'image': '',
                'alt_text': 'Test Image Alt Text',
                'default_image': True,
                'is_active': True
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

    def test_delete_product_ajax_post_view_user_logged_out(self):
        """Test delete product ajax post view user logged out"""
        response = self.client.post(self.delete_product_image_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_product_ajax_post_view_without_access(self):
        """Test delete product ajax post view without access"""
        self.client.force_login(self.user)
        response = self.client.post(self.delete_product_image_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_product_ajax_post_view_with_access(self):
        """Test delete product image ajax post view with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        # count products
        self.assertEqual(ProductImage.objects.count(), 1)
        response = self.client.post(
            self.delete_product_image_url,
            {
                'product_id': 1,
                'image_id': 1
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        # count products
        self.assertEqual(ProductImage.objects.count(), 0)

    def test_delete_product_ajax_post_view_with_access_failed(self):
        """Test delete product image view with access failed"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.delete_product_image_url,
            {
                'product_id': self.product1.id,
                'image_id': 1
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        # count products
        self.assertEqual(ProductImage.objects.count(), 1)

    def test_product_inventory_details_view_user_logged_out(self):
        """Test product inventory details view user logged out"""
        response = self.client.get(self.product_inventory_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_product_inventory_details_view_without_access(self):
        """Test product inventory details view without access"""
        self.client.force_login(self.user)
        response = self.client.get(self.product_inventory_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_product_inventory_details_view_with_access(self):
        """Test product inventory details view with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.product_inventory_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/product_inventory_details.html'
        )

    def test_product_inventory_details_view_in_promotion_with_access(self):
        """Test product inventory details view in promotion with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.promotion.products_inventory_in_promotion.add(
            self.product_inventory1
        )
        self.promotion.save()
        response = self.client.get(self.product_inventory_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/product_inventory_details.html'
        )

    def test_add_product_inventory_view_user_logged_out(self):
        """Test add product inventory view user logged out"""
        response = self.client.get(self.add_product_inventory_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_product_inventory_view_without_access(self):
        """Test add product inventory view without access"""
        self.client.force_login(self.user)
        response = self.client.get(self.add_product_inventory_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_product_inventory_view_with_access(self):
        """Test add product inventory view with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.add_product_inventory_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/add_product_inventory_details.html'
        )

    def test_get_type_attribute_ajax_post_view_user_logged_out(self):
        """Test get type attribute ajax post view user logged out"""
        response = self.client.post(
            self.get_type_attribute_url,
            {
                'type_id': 1
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_get_type_attribute_ajax_post_view_without_access(self):
        """Test get type attribute ajax post view without access"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.get_type_attribute_url,
            {
                'type_id': 1
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_get_type_attribute_ajax_post_view_with_access(self):
        """Test get type attribute ajax post view with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.get_type_attribute_url,
            {
                'type_id': 1
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

    def test_get_type_attribute_ajax_post_view_with_access_failed(self):
        """Test get type attribute ajax post view with access failed"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.get_type_attribute_url,
            {
                'type_id': 0
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

    def test_product_inventory_create_view_user_logged_out(self):
        """Test product inventory create view user logged out"""
        response = self.client.post(
            self.product_inventory_create_url,
            data={
                'sku': 2222,
                'upc': 2222,
                'product': 1,
                'product_type': 1,
                'attribute_values': [
                    '{"color":"red","women clothing size":"xs"}'
                ],
                'retail_price': ['100'],
                'store_price': ['120'],
                'sale_price': ['110'],
                'weight': ['900'],
                'active': ['true']
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_product_inventory_create_view_without_access(self):
        """Test product inventory create view without access"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.product_inventory_create_url,
            data={
                'sku': 2222,
                'upc': 2222,
                'product': 1,
                'product_type': 1,
                'attribute_values': [
                    '{"color":"red","women clothing size":"xs"}'
                ],
                'retail_price': ['100'],
                'store_price': ['120'],
                'sale_price': ['110'],
                'weight': ['900'],
                'active': ['true']
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_product_inventory_create_view_with_access_no_values(self):
        """Test product inventory create view with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.product_inventory_create_url,
            data={
                'sku': 2222,
                'upc': 2222,
                'product': 1,
                'product_type': 1,
                'attribute_values': ['{}'],
                'retail_price': ['100'],
                'store_price': ['120'],
                'sale_price': ['110'],
                'weight': ['900'],
                'active': ['true']
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(
            response.json()['success_message'],
            'Product inventory added successfully',
        )

    def test_product_inventory_create_view_with_access(self):
        """Test product inventory create view with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.product_inventory_create_url,
            data={
                'sku': 2222,
                'upc': 2222,
                'product': 1,
                'product_type': 1,
                'attribute_values': [
                    '{"color":"red","women clothing size":"xs"}'
                ],
                'retail_price': ['100'],
                'store_price': ['120'],
                'sale_price': ['110'],
                'weight': ['900'],
                'active': ['true']
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(
            response.json()['success_message'],
            'Product inventory added successfully',
        )

    def test_product_inventory_create_view_with_access_failed(self):
        """Test if the AJAX failed"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.product_inventory_create_url,
            data={
                'sku': 2222,
                'upc': 2222,
                'product': 1,
                'product_type': 1,
                'attribute_values': [
                    '{"color":"red","women clothing size":"xs"}'
                ],
                'retail_price': ['100'],
                'store_price': ['120'],
                'sale_price': ['110'],
                'weight': ['900'],
                'active': ['true']
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

    def test_product_inventory_update_view_pi_exist(self):
        """Test product inventory update view pi exist"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.product_inventory_create_url,
            data={
                'csrfmiddlewaretoken': 'LRtDcXPWz1Ibje4CuGjs9T0BXp1LBILuDkq4M6zoAezKed0Kq9fLZ4T3h9F9JSXI',
                'sku': 11111,
                'upc': 2222,
                'product': 1,
                'product_type': 1,
                'attribute_values': ['{"Color":"red","size-shoes":"35"}'],
                'retail_price': ['100'],
                'store_price': ['120'],
                'sale_price': ['110'],
                'weight': ['900'],
                'active': ['true']
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        error_message = (
            'Error adding product inventory. '
            'Error: '
            'UNIQUE constraint failed: inventory_productinventory.sku'
            ' Please check unique fields.'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(
            response.json()['error_message'],
            error_message,
        )

    def test_edit_product_inventory_view_user_logged_out(self):
        """Test add product inventory view user logged out"""
        response = self.client.get(self.edit_product_inventory_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_product_inventory_view_user_logged_in(self):
        """Test add product inventory view user logged in"""
        self.client.force_login(self.user2)
        response = self.client.get(self.edit_product_inventory_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_product_inventory_view__with_access(self):
        """Test add product inventory view with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.edit_product_inventory_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/edit_product_inventory.html'
        )
        self.client.logout()

    def test_product_inventory_update_view_user_logged_out(self):
        """Test product inventory update view user logged out"""
        response = self.client.post(
            self.product_inventory_update_url,
            data={
                'inventory_id': 1,
                'sku': 11111,
                'upc': 2222,
                'product': 1,
                'product_type': 1,
                'attribute_values': ['{"Color":"red","size-shoes":"35"}'],
                'retail_price': ['100'],
                'store_price': ['120'],
                'sale_price': ['110'],
                'weight': ['900'],
                'active': ['true']
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_product_inventory_update_view_user_without_access(self):
        """Test product inventory update view user logged in"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.product_inventory_update_url,
            data={
                'inventory_id': 1,
                'sku': 11111,
                'upc': 2222,
                'product': 1,
                'product_type': 1,
                'attribute_values': ['{"Color":"red","size-shoes":"35"}'],
                'retail_price': ['100'],
                'store_price': ['120'],
                'sale_price': ['110'],
                'weight': ['900'],
                'active': ['true']
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_product_inventory_update_view_user_with_access(self):
        """Test product inventory update view user logged in"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.product_inventory_update_url,
            data={
                'inventory_id': 1,
                'sku': 11111,
                'upc': 2222,
                'product': 1,
                'product_type': 1,
                'attribute_values': ['{"Color":"red","size-shoes":"35"}'],
                'retail_price': ['100'],
                'store_price': ['120'],
                'sale_price': ['110'],
                'weight': ['900'],
                'active': ['true']
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.client.logout()

    def test_product_inventory_update_view_user_with_access_not_values(self):
        """Test product inventory update view user logged in"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.product_inventory_update_url,
            data={
                'inventory_id': 1,
                'sku': 11111,
                'upc': 2222,
                'product': 1,
                'product_type': 1,
                'attribute_values': ['{}'],
                'retail_price': ['100'],
                'store_price': ['120'],
                'sale_price': ['110'],
                'weight': ['900'],
                'active': ['true']
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(
            response.json()['success_message'],
            'Product inventory updated successfully',
        )
        self.client.logout()

    def test_product_inventory_update_view_user_with_access_failed(self):
        """Test product inventory update view user logged in"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.product_inventory_update_url,
            data={
                'inventory_id': 1,
                'sku': 11111,
                'upc': 2222,
                'product': 1,
                'product_type': 1,
                'attribute_values': ['{"Color":"red","size-shoes":"35"}'],
                'retail_price': ['100'],
                'store_price': ['120'],
                'sale_price': ['110'],
                'weight': ['900'],
                'active': ['true']
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.client.logout()

    def test_product_inventory_update_view_user_with_access_error(self):
        """Test if there is an error in the form"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.product_inventory_update_url,
            data={
                'inventory_id': 1,
                'sku': 11111,
                'upc': 2222,
                'product': 1,
                'product_type': 1,
                'attribute_values': ['{"Color":"red","size-shoes":"35"}'],
                'retail_price': ['100'],
                'store_price': ['120'],
                'sale_price': ['110'],
                'weight': ['900'],
                'active': ['true']
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        error_message = (
            'Error updating product inventory. '
            'Error: '
            'ProductAttribute matching query does not exist.'
            ' Please check unique fields.'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(
            response.json()['error_message'],
            error_message,
        )
        self.client.logout()