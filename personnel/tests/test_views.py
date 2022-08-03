"""Test Inventory views."""
from django.test import TestCase, Client
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
            kwargs={'pk': 1, }
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
        self.delete_product_inventory_url = reverse(
            'delete_product_inventory',
            kwargs={'pk': 1, 'inventory_pk': 1}
        )
        self.product_inventories_table_url = reverse(
            'product_inventories_table',
        )
        self.categories_table_url = reverse('categories_table')
        self.add_category_url = reverse('add_category')
        self.edit_category_url = reverse(
            'edit_category',
            kwargs={'category_pk': 1}
        )
        self.delete_category_url = reverse(
            'delete_category',
            kwargs={'category_pk': 1}
        )
        self.brands_table_url = reverse('brands_table')
        self.brand_detail_url = reverse(
            'brand_detail',
            kwargs={'brand_pk': 1}
        )
        self.add_brand_url = reverse('add_brand')
        self.edit_brand_url = reverse(
            'edit_brand',
            kwargs={'brand_pk': 1}
        )
        self.delete_brand_url = reverse(
            'delete_brand',
            kwargs={'brand_pk': 1}
        )
        self.tags_table_url = reverse('tags_table')
        self.tag_detail_url = reverse(
            'tag_detail',
            kwargs={'tag_pk': 1}
        )
        self.add_tag_url = reverse('add_tag')
        self.edit_tag_url = reverse(
            'edit_tag',
            kwargs={'tag_pk': 1}
        )
        self.delete_tag_url = reverse(
            'delete_tag',
            kwargs={'tag_pk': 1}
        )
        self.stock_url = reverse('stock')
        self.add_stock_url = reverse(
            'add_stock',
            kwargs={'pk': 1, 'inventory_pk': 1}
        )
        self.update_stock_url = reverse(
            'update_stock',
            kwargs={'pk': 1, 'inventory_pk': 1, 'stock_pk': 1}
        )
        self.delete_stock_url = reverse(
            'delete_stock',
            kwargs={'pk': 1, 'inventory_pk': 1, 'stock_pk': 1}
        )
        self.product_types_table_url = reverse('product_types_table')
        self.add_product_type_url = reverse('add_product_type')
        self.edit_product_type_url = reverse(
            'edit_product_type',
            kwargs={'pk': 1}
        )
        self.delete_product_type_url = reverse(
            'delete_product_type',
            kwargs={'pk': 1}
        )
        self.product_type_attributes_url = reverse(
            'product_type_attributes'
        )
        self.add_attribute_url = reverse('add_attribute')
        self.edit_attribute_url = reverse(
            'edit_attribute',
            kwargs={'pk': 1}
        )
        self.delete_attribute_url = reverse(
            'delete_attribute',
            kwargs={'pk': 1}
        )
        self.attribute_values_url = reverse(
            'attribute_values'
        )
        self.add_attribute_value_url = reverse(
            'add_attribute_value'
        )
        self.edit_attribute_value_url = reverse(
            'edit_attribute_value',
            kwargs={'pk': 1}
        )
        self.delete_attribute_value_url = reverse(
            'delete_attribute_value',
            kwargs={'pk': 1}
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

    def test_products_table_view_with_access_search_query(self):
        """Test products table view with access search query."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.products_table_url,
            {'search_query': 'nike'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 2)
        self.assertTemplateUsed(response, 'personnel/products_table.html')

    def test_products_table_view_with_access_search_query_empty(self):
        """Test products table view with access search query empty."""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.products_table_url,
            {'search_query': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 4)
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
                'csrfmiddlewaretoken': 'LRtDcXPWz1Ibje4CuGjs9T0BXp' +
                '1LBILuDkq4M6zoAezKed0Kq9fLZ4T3h9F9JSXI',
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
        # Create new product_attr_value
        self.product_attr_value3 = ProductAttributeValue.objects.create(
            product_attribute=self.product_attribute2,
            attribute_value='s'
        )
        response = self.client.post(
            self.product_inventory_update_url,
            data={
                'inventory_id': 1,
                'sku': 11111,
                'upc': 2222,
                'product': 1,
                'product_type': 1,
                'attribute_values': [
                    '{"color":"red","women clothing size":"s"}'
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
            'Product inventory updated successfully',
        )
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
                'sku': '',
                'upc': 2222,
                'product': 1,
                'product_type': 1,
                'attribute_values': [
                    '{"Color":"red","women clothing size":"xs"}'
                ],
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

    def test_delete_product_inventory_get_view_user_logged_out(self):
        """Test delete product inventory get view user logged out"""
        response = self.client.get(
            self.delete_product_inventory_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_product_inventory_get_view_user_logged_in(self):
        """Test delete product inventory get view user logged in"""
        self.client.force_login(self.user2)
        response = self.client.get(
            self.delete_product_inventory_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_product_inventory_get_view_with_access(self):
        """Test delete product inventory get view user logged in"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.delete_product_inventory_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/delete_product_inventory.html'
        )
        self.client.logout()

    def test_delete_product_inventory_post_view_user_logged_out(self):
        """Test delete product inventory post view user logged out"""
        response = self.client.post(
            self.delete_product_inventory_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_product_inventory_post_view_without_access(self):
        """Test delete product inventory post view user without access"""
        self.client.force_login(self.user2)
        response = self.client.post(
            self.delete_product_inventory_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_product_inventory_post_view_with_access(self):
        """Test delete product inventory post view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        # check count of product inventory
        self.assertEqual(ProductInventory.objects.count(), 2)
        response = self.client.post(
            self.delete_product_inventory_url,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductInventory.objects.count(), 1)
        self.client.logout()

    def test_product_inventories_table_view_user_logged_out(self):
        """Test product inventories table view user logged out"""
        response = self.client.get(
            self.product_inventories_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_product_inventories_table_view_user_logged_in(self):
        """Test product inventories table view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.product_inventories_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_product_inventories_table_view_user_with_access(self):
        """Test product inventories table view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.product_inventories_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/product_inventories_table.html'
        )
        self.client.logout()

    def test_product_inventories_table_staff_query_search(self):
        """Test product inventories table staff query search"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.product_inventories_table_url,
            {'search_query': '11111'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/product_inventories_table.html'
        )
        self.assertEqual(len(response.context['inventories']), 1)
        self.client.logout()

    def test_product_inventories_table_staff_query_search_empty(self):
        """Test product inventories table staff query search empty"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.product_inventories_table_url,
            {'search_query': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/product_inventories_table.html'
        )
        self.assertEqual(len(response.context['inventories']), 2)
        self.client.logout()

    def test_categories_table_view_user_logged_out(self):
        """Test categories table view user logged out"""
        response = self.client.get(
            self.categories_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_categories_table_view_user_logged_in(self):
        """Test categories table view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.categories_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_categories_table_view_user_with_access(self):
        """Test categories table view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.categories_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/categories_table.html'
        )
        self.client.logout()

    def test_add_category_get_view_user_logged_out(self):
        """Test add category get view user logged out"""
        response = self.client.get(
            self.add_category_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_category_get_view_user_logged_in(self):
        """Test add category get view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.add_category_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_category_get_view_user_with_access(self):
        """Test add category get view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.add_category_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/add_category.html'
        )
        self.client.logout()

    def test_add_category_post_view_user_logged_out(self):
        """Test add category post view user logged out"""
        response = self.client.post(
            self.add_category_url,
            data={
                'name': 'Pets',
                'slug': 'pets',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_category_post_view_user_logged_in(self):
        """Test add category post view user logged in"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.add_category_url,
            data={
                'name': 'Pets',
                'slug': 'pets',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_category_post_view_user_with_access(self):
        """Test add category post view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.assertEqual(Category.objects.count(), 2)
        response = self.client.post(
            self.add_category_url,
            data={
                'name': 'Pets',
                'slug': 'pets',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 3)
        self.client.logout()

    def test_add_category_post_view_user_with_access_failed(self):
        """Test add category post view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.assertEqual(Category.objects.count(), 2)
        response = self.client.post(
            self.add_category_url,
            data={
                'name': '',
                'slug': 'pets',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 2)
        self.client.logout()

    def test_edit_category_get_view_user_logged_out(self):
        """Test edit category get view user logged out"""
        response = self.client.get(
            self.edit_category_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_category_get_view_user_logged_in(self):
        """Test edit category get view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.edit_category_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_category_get_view_user_with_access(self):
        """Test edit category get view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.edit_category_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/edit_category.html'
        )
        self.client.logout()

    def test_edit_category_post_view_user_logged_out(self):
        """Test edit category post view user logged out"""
        response = self.client.post(
            self.edit_category_url,
            data={
                'name': 'Pets',
                'slug': 'pets',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_category_post_view_user_logged_in(self):
        """Test edit category post view user logged in"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.edit_category_url,
            data={
                'name': 'Pets',
                'slug': 'pets',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_category_post_view_user_with_access(self):
        """Test edit category post view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.assertEqual(Category.objects.count(), 2)
        response = self.client.post(
            self.edit_category_url,
            data={
                'name': 'Pets',
                'slug': 'pets',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 2)
        self.client.logout()

    def test_edit_category_post_view_user_with_access_failed(self):
        """Test edit category post view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.assertEqual(Category.objects.count(), 2)
        response = self.client.post(
            self.edit_category_url,
            data={
                'name': '',
                'slug': 'pets',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 2)
        self.client.logout()

    def test_delete_category_get_view_user_logged_out(self):
        """Test delete category get view user logged out"""
        response = self.client.get(
            self.delete_category_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_category_get_view_user_logged_in(self):
        """Test delete category get view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.delete_category_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_category_get_view_staff_without_access(self):
        """Test delete category get view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.delete_category_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_category_get_view_user_with_access(self):
        """Test delete category get view user with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        self.assertEqual(Category.objects.count(), 2)
        response = self.client.get(
            self.delete_category_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/delete_category.html'
        )
        self.client.logout()

    def test_delete_category_post_view_user_logged_out(self):
        """Test delete category post view user logged out"""
        response = self.client.post(
            self.delete_category_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_category_post_view_user_logged_in(self):
        """Test delete category post view user logged in"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.delete_category_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_category_post_view_staff_without_access(self):
        """Test delete category post view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.assertEqual(Category.objects.count(), 2)
        response = self.client.post(
            self.delete_category_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_category_post_view_user_with_access(self):
        """Test delete category post view user with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        self.assertEqual(Category.objects.count(), 2)
        response = self.client.post(
            self.delete_category_url,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 1)
        self.client.logout()

    def test_delete_category_post_view_user_with_access_failed(self):
        """Test delete category post view user with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        self.delete_category_url = reverse(
            'delete_category',
            kwargs={'category_pk': 0}
        )
        self.assertEqual(Category.objects.count(), 2)
        response = self.client.post(
            self.delete_category_url,
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Category.objects.count(), 2)
        self.client.logout()

    def test_brands_table_get_view_user_logged_out(self):
        """Test brands table get view user logged out"""
        response = self.client.get(
            self.brands_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_brands_table_get_view_user_logged_in(self):
        """Test brands table get view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.brands_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_brands_table_get_view_staff_with_access(self):
        """Test brands table get view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.brands_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/brands_table.html')
        self.client.logout()

    def test_brands_table_get_view_staff_search_query(self):
        """Test brands table get view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.brands_table_url,
            {'search_query': 'Nike'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/brands_table.html')
        self.assertEqual(len(response.context['brands']), 1)
        self.client.logout()

    def test_brands_table_get_view_staff_search_query_no_results(self):
        """Test brands table get view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.brands_table_url,
            {'search_query': ''},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/brands_table.html')
        self.assertEqual(len(response.context['brands']), 2)
        self.client.logout()

    def test_brand_detail_view_user_logged_out(self):
        """Test brand detail view user logged out"""
        response = self.client.get(
            self.brand_detail_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_brand_detail_view_user_logged_in(self):
        """Test brand detail view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.brand_detail_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_brand_detail_view_staff_with_access(self):
        """Test brand detail view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.brand_detail_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/brand_detail.html')
        self.client.logout()

    def test_add_brand_get_view_user_logged_out(self):
        """Test add brand get view user logged out"""
        response = self.client.get(
            self.add_brand_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_brand_get_view_user_logged_in(self):
        """Test add brand get view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.add_brand_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_brand_get_view_staff_with_access(self):
        """Test add brand get view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.add_brand_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/add_brand.html')
        self.client.logout()

    def test_add_brand_post_view_user_logged_out(self):
        """Test add brand post view user logged out"""
        response = self.client.post(
            self.add_brand_url,
            data={
                'name': 'Brand',
                'description': 'Brand description',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_brand_post_view_user_logged_in(self):
        """Test add brand post view user logged in"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.add_brand_url,
            data={
                'name': 'Brand',
                'description': 'Brand description',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_brand_post_view_staff_with_access(self):
        """Test add brand post view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.add_brand_url,
            data={
                'name': 'Brand',
                'description': 'Brand description',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Brand.objects.count(), 3)
        self.client.logout()

    def test_add_brand_post_view_staff_with_access_invalid(self):
        """Test add brand post view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.add_brand_url,
            data={
                'name': '',
                'description': 'Brand description',
                'is_active': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Brand.objects.count(), 2)
        self.assertTemplateUsed(response, 'personnel/add_brand.html')
        self.client.logout()

    def test_edit_brand_get_view_user_logged_out(self):
        """Test edit brand get view user logged out"""
        response = self.client.get(
            self.edit_brand_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_brand_get_view_user_logged_in(self):
        """Test edit brand get view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.edit_brand_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_brand_get_view_staff_with_access(self):
        """Test edit brand get view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.edit_brand_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/edit_brand.html')
        self.client.logout()

    def test_edit_brand_post_view_user_logged_out(self):
        """Test edit brand post view user logged out"""
        response = self.client.post(
            self.edit_brand_url,
            data={
                'name': 'Brand',
                'description': 'Brand description',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_brand_post_view_user_logged_in(self):
        """Test edit brand post view user logged in"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.edit_brand_url,
            data={
                'name': 'Brand',
                'description': 'Brand description',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_brand_post_view_staff_with_access(self):
        """Test edit brand post view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.assertEqual(Brand.objects.count(), 2)
        self.profile2.save()
        response = self.client.post(
            self.edit_brand_url,
            data={
                'name': 'Brand3',
                'description': 'Brand description',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Brand.objects.count(), 2)
        self.client.logout()

    def test_edit_brand_post_view_staff_with_access_invalid(self):
        """Test edit brand post view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.assertEqual(Brand.objects.count(), 2)
        self.profile2.save()
        response = self.client.post(
            self.edit_brand_url,
            data={
                'name': '',
                'description': 'Brand description',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Brand.objects.count(), 2)
        self.assertTemplateUsed(response, 'personnel/edit_brand.html')
        self.client.logout()

    def test_delete_brand_get_view_user_logged_out(self):
        """Test delete brand get view user logged out"""
        response = self.client.get(
            self.delete_brand_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_brand_get_view_user_logged_in(self):
        """Test delete brand get view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.delete_brand_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_brand_get_view_staff_without_access(self):
        """Test delete brand get view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.delete_brand_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_brand_get_view_admin_with_access(self):
        """Test delete brand post view admin with access"""
        self.client.force_login(self.user3)
        self.assertTrue(self.profile3.role.id == 3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(
            self.delete_brand_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/delete_brand.html')
        self.client.logout()

    def test_delete_brand_post_view_user_logged_out(self):
        """Test delete brand post view user logged out"""
        response = self.client.post(
            self.delete_brand_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_brand_post_view_user_logged_in(self):
        """Test delete brand post view user logged in"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.delete_brand_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_brand_post_view_staff_without_access(self):
        """Test delete brand post view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.delete_brand_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_brand_post_view_admin_with_access(self):
        """Test delete brand post view user with access"""
        self.client.force_login(self.user3)
        self.assertTrue(self.profile3.role.id == 3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.post(
            self.delete_brand_url,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Brand.objects.count(), 1)
        self.client.logout()

    def test_tags_table_view_user_logged_out(self):
        """Test tags table view user logged out"""
        response = self.client.get(
            self.tags_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_tags_table_view_user_logged_in(self):
        """Test tags table view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.tags_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_tags_table_view_staff_with_access(self):
        """Test tags table view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.tags_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/tags_table.html')
        self.client.logout()

    def test_tags_table_view_staff_search_query(self):
        """Test tags table view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.tags_table_url,
            {'search_query': 'skirt'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/tags_table.html')
        self.assertEqual(len(response.context['tags']), 1)
        self.client.logout()

    def test_tags_table_view_staff_search_query_empty(self):
        """Test tags table view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.tags_table_url,
            {'search_query': ''},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/tags_table.html')
        self.assertEqual(len(response.context['tags']), 2)
        self.client.logout()

    def test_tag_details_view_user_logged_out(self):
        """Test tag details view user logged out"""
        response = self.client.get(
            self.tag_detail_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_tag_details_view_user_logged_in(self):
        """Test tag details view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.tag_detail_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_tag_details_view_staff_with_access(self):
        """Test tag details view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.tag_detail_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/tag_detail.html')
        self.client.logout()

    def test_add_tag_view_user_logged_out(self):
        """Test add tag view user logged out"""
        response = self.client.get(
            self.add_tag_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_tag_view_user_logged_in(self):
        """Test add tag view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.add_tag_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_tag_view_staff_with_access(self):
        """Test add tag view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.add_tag_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/add_tag.html')
        self.client.logout()

    def test_add_tag_post_view_user_logged_out(self):
        """Test add tag post view user logged out"""
        response = self.client.post(
            self.add_tag_url,
            data={
                'name': 'Test Tag',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_tag_post_view_user_logged_in(self):
        """Test add tag post view user logged in"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.add_tag_url,
            data={
                'name': 'Test Tag',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_tag_post_view_staff_with_access(self):
        """Test add tag post view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.assertEqual(Tag.objects.count(), 2)
        response = self.client.post(
            self.add_tag_url,
            data={
                'name': 'Test Tag',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tag.objects.count(), 3)
        self.client.logout()

    def test_add_tag_post_view_staff_with_access_failed(self):
        """Test add tag post view user with access failed"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.add_tag_url,
            data={
                'name': '',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/add_tag.html')
        self.client.logout()

    def test_edit_tag_view_user_logged_out(self):
        """Test edit tag view user logged out"""
        response = self.client.get(
            self.edit_tag_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_tag_view_user_logged_in(self):
        """Test edit tag view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.edit_tag_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_tag_view_staff_with_access(self):
        """Test edit tag view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.edit_tag_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/edit_tag.html')
        self.client.logout()

    def test_edit_tag_post_view_user_logged_out(self):
        """Test edit tag post view user logged out"""
        response = self.client.post(
            self.edit_tag_url,
            data={
                'name': 'Test Tag',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_tag_post_view_user_logged_in(self):
        """Test edit tag post view user logged in"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.edit_tag_url,
            data={
                'name': 'Test Tag',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_tag_post_view_staff_with_access(self):
        """Test edit tag post view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.assertEqual(Tag.objects.count(), 2)
        response = self.client.post(
            self.edit_tag_url,
            data={
                'name': 'Test Tag',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tag.objects.count(), 2)
        self.client.logout()

    def test_edit_tag_post_view_staff_with_access_failed(self):
        """Test edit tag post view user with access failed"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.edit_tag_url,
            data={
                'name': '',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/edit_tag.html')
        self.client.logout()

    def test_delete_tag_view_user_logged_out(self):
        """Test delete tag view user logged out"""
        response = self.client.get(
            self.delete_tag_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_tag_view_user_logged_in(self):
        """Test delete tag view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.delete_tag_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_tag_view_staff_with_access(self):
        """Test delete tag view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.delete_tag_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/delete_tag.html')
        self.client.logout()

    def test_delete_tag_post_view_user_logged_out(self):
        """Test delete tag post view user logged out"""
        response = self.client.post(
            self.delete_tag_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_tag_post_view_user_logged_in(self):
        """Test delete tag post view user logged in"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.delete_tag_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_tag_post_view_staff_with_access(self):
        """Test delete tag post view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.assertEqual(Tag.objects.count(), 2)
        response = self.client.post(
            self.delete_tag_url,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tag.objects.count(), 1)
        self.client.logout()

    def test_stock_view_user_logged_out(self):
        """Test stock view user logged out"""
        response = self.client.get(
            self.stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_stock_view_user_logged_in(self):
        """Test stock view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_stock_view_staff_with_access(self):
        """Test stock view user with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/stock.html')
        self.client.logout()

    def test_stock_view_staff_with_access_sort_all(self):
        """Test stock view user with access sort all"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        # create stock for self.product_inventory1
        Stock.objects.create(
            product_inventory=self.product_inventory1,
            units_variable=50,
            units=40,
            units_sold=9
        )
        response = self.client.get(
            self.stock_url,
            data={
                'sort': 'all',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/stock.html')
        self.assertEqual(len(response.context['all_stock']), 1)
        self.client.logout()

    def test_stock_view_staff_with_access_sort_inconsistency(self):
        """Test stock view user with access sort inconsistency"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        # create stock for self.product_inventory1
        Stock.objects.create(
            product_inventory=self.product_inventory1,
            units_variable=50,
            units=40,
            units_sold=9
        )
        response = self.client.get(
            self.stock_url,
            data={
                'sort': 'inconsistency',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/stock.html')
        self.assertEqual(len(response.context['all_stock']), 1)
        self.client.logout()

    def test_stock_view_staff_with_access_sort_high_sales_fewer_products(self):
        """Test stock view user with access sort high sales fewer products"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        # create stock for self.product_inventory1
        Stock.objects.create(
            product_inventory=self.product_inventory1,
            units_variable=150,
            units=40,
            units_sold=110
        )
        response = self.client.get(
            self.stock_url,
            data={
                'sort': 'high-sales-lack-units',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/stock.html')
        self.assertEqual(len(response.context['all_stock']), 1)
        self.client.logout()

    def test_stock_view_staff_with_access_sort_stock_50(self):
        """Test stock view user with access sort fewer 50"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        # create stock for self.product_inventory1
        Stock.objects.create(
            product_inventory=self.product_inventory1,
            units_variable=50,
            units=40,
            units_sold=9
        )
        response = self.client.get(
            self.stock_url,
            data={
                'sort': 'stock-50',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/stock.html')
        self.assertEqual(len(response.context['all_stock']), 1)
        self.client.logout()

    def test_stock_view_staff_with_access_sort_stock_20(self):
        """Test stock view user with access sort fewer 20"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        # create stock for self.product_inventory1
        Stock.objects.create(
            product_inventory=self.product_inventory1,
            units_variable=20,
            units=19,
            units_sold=1
        )
        response = self.client.get(
            self.stock_url,
            data={
                'sort': 'stock-20',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/stock.html')
        self.assertEqual(len(response.context['all_stock']), 1)
        self.client.logout()

    def test_stock_view_staff_with_access_sort_stock_10(self):
        """Test stock view user with access sort fewer 10"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        # create stock for self.product_inventory1
        Stock.objects.create(
            product_inventory=self.product_inventory1,
            units_variable=10,
            units=9,
            units_sold=1
        )
        response = self.client.get(
            self.stock_url,
            data={
                'sort': 'stock-10',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/stock.html')
        self.assertEqual(len(response.context['all_stock']), 1)
        self.client.logout()

    def test_stock_view_staff_with_access_sort_stock_0(self):
        """Test stock view user with access sort fewer 0"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        # create stock for self.product_inventory1
        Stock.objects.create(
            product_inventory=self.product_inventory1,
            units_variable=10,
            units=0,
            units_sold=10
        )
        response = self.client.get(
            self.stock_url,
            data={
                'sort': 'stock-0',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/stock.html')
        self.assertEqual(len(response.context['all_stock']), 1)
        self.client.logout()

    def test_stock_view_staff_with_access_sort_low_sales(self):
        """Test stock view user with access sort low sales"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        # create stock for self.product_inventory1
        Stock.objects.create(
            product_inventory=self.product_inventory1,
            units_variable=550,
            units=549,
            units_sold=1
        )
        response = self.client.get(
            self.stock_url,
            data={
                'sort': 'low-sales',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/stock.html')
        self.assertEqual(len(response.context['all_stock']), 1)
        self.client.logout()

    def test_add_stock_get_view_user_logged_out(self):
        """Test add stock get view user logged out"""
        response = self.client.get(
            self.add_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_stock_get_view_user_logged_in(self):
        """Test add stock get view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.add_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_stock_get_view_staff_without_access(self):
        """Test add stock get view user without access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.add_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_stock_get_view_admin_with_access(self):
        """Test add stock get view admin with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(
            self.add_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/add_stock.html')
        self.client.logout()

    def test_add_stock_post_view_user_logged_out(self):
        """Test add stock post view user logged out"""
        response = self.client.post(
            self.add_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_stock_post_view_user_logged_in(self):
        """Test add stock post view user logged in"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.add_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_stock_post_view_staff_without_access(self):
        """Test add stock post view user without access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.add_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_stock_post_view_admin_with_access(self):
        """Test add stock post view admin with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        self.assertEqual(Stock.objects.count(), 0)
        response = self.client.post(
            self.add_stock_url,
            {
                'last_checked': '2020-01-01',
                'units_variable': 50,
                'units': 40,
                'units_sold': 10,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Stock.objects.count(), 1)
        self.client.logout()

    def test_add_stock_post_view_admin_with_access_failed(self):
        """Test add stock post view admin with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        self.assertEqual(Stock.objects.count(), 0)
        response = self.client.post(
            self.add_stock_url,
            {
                'last_checked': '2020-01-01',
                'units_variable': 50,
                'units': '',
                'units_sold': 10,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Stock.objects.count(), 0)
        self.client.logout()

    def test_update_stock_get_view_user_logged_out(self):
        """Test update stock get view user logged out"""
        response = self.client.get(
            self.update_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_update_stock_get_view_user_logged_in(self):
        """Test update stock get view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.update_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_update_stock_get_view_staff_without_access(self):
        """Test update stock get view user without access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.update_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_update_stock_get_view_admin_with_access(self):
        """Test update stock get view admin with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        self.assertEqual(Stock.objects.count(), 0)
        response = self.client.post(
            self.add_stock_url,
            {
                'last_checked': '2020-01-01',
                'units_variable': 50,
                'units': 40,
                'units_sold': 10,
            },
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(
            self.update_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/update_stock.html')
        self.client.logout()

    def test_update_stock_post_view_user_logged_out(self):
        """Test update stock post view user logged out"""
        response = self.client.post(
            self.update_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_update_stock_post_view_user_logged_in(self):
        """Test update stock post view user logged in"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.update_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_update_stock_post_view_staff_without_access(self):
        """Test update stock post view user without access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.update_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_update_stock_post_view_admin_with_access(self):
        """Test update stock post view admin with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        self.assertEqual(Stock.objects.count(), 0)
        response = self.client.post(
            self.add_stock_url,
            {
                'last_checked': '2020-01-01',
                'units_variable': 50,
                'units': 40,
                'units_sold': 10,
            },
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.post(
            self.update_stock_url,
            {
                'last_checked': '2020-01-01',
                'units_variable': 500,
                'units': 490,
                'units_sold': 10,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Stock.objects.count(), 1)
        self.client.logout()

    def test_update_stock_post_view_admin_with_access_failed(self):
        """Test update stock post view admin with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        self.assertEqual(Stock.objects.count(), 0)
        response = self.client.post(
            self.add_stock_url,
            {
                'last_checked': '2020-01-01',
                'units_variable': 50,
                'units': 40,
                'units_sold': 10,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Stock.objects.count(), 1)
        response = self.client.post(
            self.update_stock_url,
            {
                'last_checked': '2020-01-01',
                'units_variable': 500,
                'units': '',
                'units_sold': 10,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Stock.objects.count(), 1)
        self.client.logout()

    def test_delete_stock_get_view_user_logged_out(self):
        """Test delete stock get view user logged out"""
        response = self.client.get(
            self.delete_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_stock_get_view_user_logged_in(self):
        """Test delete stock get view user logged in"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.delete_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_stock_get_view_staff_without_access(self):
        """Test delete stock get view user without access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.delete_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_stock_get_view_admin_with_access(self):
        """Test delete stock get view admin with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        self.assertEqual(Stock.objects.count(), 0)
        response = self.client.post(
            self.add_stock_url,
            {
                'last_checked': '2020-01-01',
                'units_variable': 50,
                'units': 40,
                'units_sold': 10,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Stock.objects.count(), 1)
        response = self.client.get(
            self.delete_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/delete_stock.html')
        self.client.logout()

    def test_delete_stock_post_view_user_logged_out(self):
        """Test delete stock post view user logged out"""
        response = self.client.post(
            self.delete_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_stock_post_view_user_logged_in(self):
        """Test delete stock post view user logged in"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.delete_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_stock_post_view_staff_without_access(self):
        """Test delete stock post view user without access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.delete_stock_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_stock_post_view_admin_with_access(self):
        """Test delete stock post view admin with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        self.assertEqual(Stock.objects.count(), 0)
        response = self.client.post(
            self.add_stock_url,
            {
                'last_checked': '2020-01-01',
                'units_variable': 50,
                'units': 40,
                'units_sold': 10,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Stock.objects.count(), 1)
        response = self.client.post(
            self.delete_stock_url,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Stock.objects.count(), 0)
        self.client.logout()

    def test_product_types_table_view_user_logged_out(self):
        """Test product types table view user logged out"""
        response = self.client.get(
            self.product_types_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_product_types_table_view_user_logged_in_without_access(self):
        """Test product types table view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.product_types_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_product_types_table_view_user_logged_in_with_access(self):
        """Test product types table view user logged in with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.product_types_table_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/product_types_list.html')
        self.client.logout()

    def test_product_types_with_access_search_query(self):
        """Test product types with access search query"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.product_types_table_url,
            {
                'search_query': 'women clothes',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/product_types_list.html')
        self.assertEqual(len(response.context['product_types']), 1)
        self.client.logout()

    def test_product_types_with_access_search_query_empty(self):
        """Test product types with access search query empty"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.product_types_table_url,
            {
                'search_query': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/product_types_list.html')
        self.assertEqual(len(response.context['product_types']), 2)
        self.client.logout()

    def test_add_product_type_get_view_user_logged_out(self):
        """Test add product type get view user logged out"""
        response = self.client.get(
            self.add_product_type_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_product_type_get_view_user_logged_in_without_access(self):
        """Test add product type get view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.add_product_type_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_product_type_get_view_user_logged_in_with_access(self):
        """Test add product type get view user logged in with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.add_product_type_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/add_product_type.html')
        self.client.logout()

    def test_add_product_type_post_view_user_logged_out(self):
        """Test add product type post view user logged out"""
        self.assertEqual(ProductType.objects.count(), 2)
        response = self.client.post(
            self.add_product_type_url,
            {
                'name': 'Test product type',
                'product_type_attributes': [
                    self.product_attribute1.id,
                    self.product_attribute2.id,
                ],
                'description': 'Test description',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_product_type_post_view_user_logged_in_without_access(self):
        """Test add product type post view user logged in without access"""
        self.client.force_login(self.user)
        self.assertEqual(ProductType.objects.count(), 2)
        response = self.client.post(
            self.add_product_type_url,
            {
                'name': 'Test product type',
                'product_type_attributes': [
                    self.product_attribute1.id,
                    self.product_attribute2.id,
                ],
                'description': 'Test description',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_product_type_post_view_user_logged_in_with_access(self):
        """Test add product type post view user logged in with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.assertEqual(ProductType.objects.count(), 2)
        response = self.client.post(
            self.add_product_type_url,
            {
                'name': 'Test product type',
                'product_type_attributes': [
                    self.product_attribute1.id,
                    self.product_attribute2.id,
                ],
                'description': 'Test description',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductType.objects.count(), 3)
        self.client.logout()

    def test_add_product_type_post_view_user_with_access_failed(self):
        """Test add product type post view user logged in with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.assertEqual(ProductType.objects.count(), 2)
        response = self.client.post(
            self.add_product_type_url,
            {
                'name': '',
                'product_type_attributes': [
                    self.product_attribute1.id,
                    self.product_attribute2.id,
                ],
                'description': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/add_product_type.html')
        self.assertEqual(ProductType.objects.count(), 2)
        self.client.logout()

    def test_edit_product_type_get_view_user_logged_out(self):
        """Test edit product type get view user logged out"""
        response = self.client.get(
            self.edit_product_type_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_product_type_get_view_user_logged_in_without_access(self):
        """Test edit product type get view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.edit_product_type_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_product_type_get_view_user_logged_in_with_access(self):
        """Test edit product type get view user logged in with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.edit_product_type_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/edit_product_type.html')
        self.client.logout()

    def test_edit_product_type_post_view_user_logged_out(self):
        """Test edit product type post view user logged out"""
        response = self.client.post(
            self.edit_product_type_url,
            {
                'name': 'Test product type',
                'product_type_attributes': [
                    self.product_attribute1.id,
                    self.product_attribute2.id,
                ],
                'description': 'Test description',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_product_type_post_view_user_logged_in_without_access(self):
        """Test edit product type post view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.edit_product_type_url,
            {
                'name': 'Test product type',
                'product_type_attributes': [
                    self.product_attribute1.id,
                    self.product_attribute2.id,
                ],
                'description': 'Test description',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_product_type_post_view_user_logged_in_with_access(self):
        """Test edit product type post view user logged in with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.edit_product_type_url,
            {
                'name': 'Test product type',
                'product_type_attributes': [
                    self.product_attribute1.id,
                    self.product_attribute2.id,
                ],
                'description': 'Test description',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductType.objects.count(), 2)
        self.client.logout()

    def test_edit_product_type_post_view_user_with_access_failed(self):
        """Test edit product type post view user logged in with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.edit_product_type_url,
            {
                'name': '',
                'product_type_attributes': [
                    self.product_attribute1.id,
                    self.product_attribute2.id,
                ],
                'description': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/edit_product_type.html')
        self.assertEqual(ProductType.objects.count(), 2)
        self.client.logout()

    def test_delete_product_type_get_view_user_logged_out(self):
        """Test delete product type get view user logged out"""
        response = self.client.get(
            self.delete_product_type_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_product_type_get_view_user_logged_in_without_access(self):
        """Test delete product type get view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.delete_product_type_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_product_type_get_view_user_logged_in_with_access(self):
        """Test delete product type get view user logged in with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(
            self.delete_product_type_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/delete_product_type.html')
        self.client.logout()

    def test_product_type_attributes_get_view_user_logged_out(self):
        """Test product type attributes get view user logged out"""
        response = self.client.get(
            self.product_type_attributes_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_product_type_attributes_get_view_user_without_access(self):
        """
        Test product type attributes get view user
        logged in without access
        """
        self.client.force_login(self.user)
        response = self.client.get(
            self.product_type_attributes_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_product_type_attributes_get_view_in_with_access(self):
        """Test product type attributes get view user logged in with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.product_type_attributes_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/attributes_list.html')
        self.client.logout()

    def test_product_type_attribute_staff_search_query(self):
        """Test product type attribute staff search query"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.product_type_attributes_url,
            {
                'search_query': 'women clothing size',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/attributes_list.html')
        self.assertEqual(len(response.context['attributes']), 1)
        self.client.logout()

    def test_product_type_attribute_staff_search_query_empty(self):
        """Test product type attribute staff search query empty"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.product_type_attributes_url,
            {
                'search_query': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/attributes_list.html')
        self.assertEqual(len(response.context['attributes']), 2)
        self.client.logout()

    def test_add_attribute_get_view_user_logged_out(self):
        """Test add attribute get view user logged out"""
        response = self.client.get(
            self.add_attribute_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_attribute_get_view_user_without_access(self):
        """Test add attribute get view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.add_attribute_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_attribute_get_view_user_with_access(self):
        """Test add attribute get view user logged in with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.add_attribute_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/add_attribute.html')
        self.client.logout()

    def test_add_attribute_post_view_user_logged_out(self):
        """Test add attribute post view user logged out"""
        response = self.client.post(
            self.add_attribute_url,
            {
                'name': '',
                'description': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_attribute_post_view_user_without_access(self):
        """Test add attribute post view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.add_attribute_url,
            {
                'name': '',
                'description': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_attribute_post_view_user_with_access(self):
        """Test add attribute post view user logged in with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.assertEqual(ProductAttribute.objects.count(), 2)
        response = self.client.post(
            self.add_attribute_url,
            {
                'name': 'taste',
                'description': 'banana',
            },
        )
        self.assertEqual(response.status_code, 302)
        # check count
        self.assertEqual(ProductAttribute.objects.count(), 3)
        self.client.logout()

    def test_add_attribute_post_view_user_with_access_failed(self):
        """Test add attribute post view user logged in with access failed"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.add_attribute_url,
            {
                'name': '',
                'description': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/add_attribute.html')
        self.client.logout()

    def test_edit_attribute_get_view_user_logged_out(self):
        """Test edit attribute get view user logged out"""
        response = self.client.get(
            self.edit_attribute_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_attribute_get_view_user_without_access(self):
        """Test edit attribute get view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.edit_attribute_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_attribute_get_view_user_with_access(self):
        """Test edit attribute get view user logged in with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            self.edit_attribute_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/edit_attribute.html')
        self.client.logout()

    def test_edit_attribute_post_view_user_logged_out(self):
        """Test edit attribute post view user logged out"""
        response = self.client.post(
            self.edit_attribute_url,
            {
                'name': '',
                'description': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_attribute_post_view_user_without_access(self):
        """Test edit attribute post view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.edit_attribute_url,
            {
                'name': '',
                'description': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_attribute_post_view_user_with_access(self):
        """Test edit attribute post view user logged in with access"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.assertEqual(ProductAttribute.objects.count(), 2)
        response = self.client.post(
            self.edit_attribute_url,
            {
                'name': 'taste',
                'description': 'banana',
            },
        )
        self.assertEqual(response.status_code, 302)
        # check count
        self.assertEqual(ProductAttribute.objects.count(), 2)
        self.client.logout()

    def test_edit_attribute_post_view_user_with_access_failed(self):
        """Test edit attribute post view user logged in with access failed"""
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.edit_attribute_url,
            {
                'name': '',
                'description': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/edit_attribute.html')
        self.client.logout()

    def test_delete_attribute_get_view_user_logged_out(self):
        """Test delete attribute get view user logged out"""
        response = self.client.get(
            self.delete_attribute_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_attribute_get_view_user_without_access(self):
        """Test delete attribute get view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.delete_attribute_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_attribute_get_view_user_with_access(self):
        """Test delete attribute get view user logged in with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(self.delete_attribute_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personnel/delete_attribute.html')

    def test_attribute_values_get_view_user_logged_out(self):
        """Test attribute values get view user logged out"""
        response = self.client.get(
            self.attribute_values_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_attribute_values_get_view_user_without_access(self):
        """Test attribute values get view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.attribute_values_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_attribute_values_get_view_user_with_access(self):
        """Test attribute values get view user logged in with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(self.attribute_values_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/attribute_values_list.html'
        )

    def test_attribute_values_staff_query_search(self):
        """Test attribute values staff query search"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(
            self.attribute_values_url,
            {
                'search_query': 'red',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/attribute_values_list.html'
        )
        self.assertEqual(len(response.context['attribute_values']), 1)

    def test_attribute_values_staff_query_search_empty(self):
        """Test attribute values staff query search empty"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(
            self.attribute_values_url,
            {
                'search_query': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/attribute_values_list.html'
        )
        self.assertEqual(len(response.context['attribute_values']), 2)

    def test_add_attribute_value_get_view_user_logged_out(self):
        """Test add attribute value get view user logged out"""
        response = self.client.get(
            self.add_attribute_value_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_attribute_value_get_view_user_without_access(self):
        """Test add attribute value get view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.add_attribute_value_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_attribute_value_get_view_user_with_access(self):
        """Test add attribute value get view user logged in with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(self.add_attribute_value_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/add_attribute_value.html'
        )

    def test_add_attribute_value_post_view_user_logged_out(self):
        """Test add attribute value post view user logged out"""
        response = self.client.post(
            self.add_attribute_value_url,
            {
                'product_attribute': self.product_attribute1.id,
                'attribute_value': 'banana',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_attribute_value_post_view_user_without_access(self):
        """Test add attribute value post view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.add_attribute_value_url,
            {
                'product_attribute': self.product_attribute1.id,
                'attribute_value': 'banana',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_attribute_value_post_view_user_with_access(self):
        """Test add attribute value post view user logged in with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        # count the number of attribute values before adding
        self.assertTrue(ProductAttributeValue.objects.count() == 2)
        response = self.client.post(
            self.add_attribute_value_url,
            {
                'product_attribute': self.product_attribute1.id,
                'attribute_value': 'banana',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ProductAttributeValue.objects.count() == 3)

    def test_add_attribute_value_post_view_user_with_access_failed(self):
        """Test add attribute value post view user logged in with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        # count the number of attribute values before adding
        self.assertTrue(ProductAttributeValue.objects.count() == 2)
        response = self.client.post(
            self.add_attribute_value_url,
            {
                'product_attribute': '',
                'attribute_value': 'banana',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ProductAttributeValue.objects.count() == 2)

    def test_edit_attribute_value_get_view_user_logged_out(self):
        """Test edit attribute value get view user logged out"""
        response = self.client.get(
            self.edit_attribute_value_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_attribute_value_get_view_user_without_access(self):
        """Test edit attribute value get view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.edit_attribute_value_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_attribute_value_get_view_user_with_access(self):
        """Test edit attribute value get view user logged in with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(self.edit_attribute_value_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/edit_attribute_value.html'
        )

    def test_edit_attribute_value_post_view_user_logged_out(self):
        """Test edit attribute value post view user logged out"""
        response = self.client.post(
            self.edit_attribute_value_url,
            {
                'product_attribute': self.product_attribute1.id,
                'attribute_value': 'banana',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_attribute_value_post_view_user_without_access(self):
        """Test edit attribute value post view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.post(
            self.edit_attribute_value_url,
            {
                'product_attribute': self.product_attribute1.id,
                'attribute_value': 'banana',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_attribute_value_post_view_user_with_access(self):
        """Test edit attribute value post view user logged in with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        # count the number of attribute values before adding
        self.assertTrue(ProductAttributeValue.objects.count() == 2)
        response = self.client.post(
            self.edit_attribute_value_url,
            {
                'product_attribute': self.product_attribute1.id,
                'attribute_value': 'banana',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ProductAttributeValue.objects.count() == 2)

    def test_edit_attribute_value_post_view_user_with_access_failed(self):
        """Test edit attribute value post view user logged in with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        # count the number of attribute values before adding
        self.assertTrue(ProductAttributeValue.objects.count() == 2)
        response = self.client.post(
            self.edit_attribute_value_url,
            {
                'product_attribute': '',
                'attribute_value': 'banana',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ProductAttributeValue.objects.count() == 2)

    def test_delete_attribute_value_get_view_user_logged_out(self):
        """Test delete attribute value get view user logged out"""
        response = self.client.get(
            self.delete_attribute_value_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_attribute_value_get_view_user_without_access(self):
        """Test delete value get view user logged in without access"""
        self.client.force_login(self.user)
        response = self.client.get(
            self.delete_attribute_value_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_attribute_value_get_view_user_with_access(self):
        """Test delete attribute value get view user logged in with access"""
        self.client.force_login(self.user3)
        self.assertFalse(self.profile3.role.id == 2)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(self.delete_attribute_value_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'personnel/delete_attribute_value.html'
        )
