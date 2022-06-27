"""Tests for promotions views."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import Role, Profile
from promotions.models import Promotion
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
from datetime import datetime
from django.utils import timezone

class PromotionsListViewTest(TestCase):
    """Tests for the promotions list view."""

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
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        print(self.profile2.role.id)
        print(self.profile2.role)
        print(self.profile2.user)
        self.profile1 = Profile.objects.get(id=self.user.profile.id)
        print(self.profile1.role.id)
        print(self.profile1.role)
        print(self.profile1.user)
        # Create products
        # self.category1 = Category.objects.create(
        #     name='Clothing',
        #     slug='clothing',
        #     is_active=False,
        # )
        # self.category2 = Category.objects.create(
        #     name='Food',
        #     slug='food',
        #     is_active=True,
        # )
        # self.tag1 = Tag.objects.create(
        #     name='skirt',
        #     slug='skirt',
        #     is_active=True,
        # )
        # self.tag2 = Tag.objects.create(
        #     name='shirt',
        #     slug='shirt',
        #     is_active=False,
        # )
        # self.brand1 = Brand.objects.create(
        #     name='Nike',
        #     slug='nike',
        #     is_active=True,
        # )
        # self.brand2 = Brand.objects.create(
        #     name='Adidas',
        #     slug='adidas',
        #     is_active=False,
        # )
        # self.product1 = Product.objects.create(
        #     name='Nike Skirt',
        #     slug='nike-skirt',
        #     description='Nike Skirt',
        #     category=self.category1,
        #     brand=self.brand1,
        #     is_active=True,
        # )
        # self.product1.tags.add(self.tag1)
        # self.product2 = Product.objects.create(
        #     name='Adidas Shirt',
        #     slug='Adidas-Shirt',
        #     description='Adidas Shirt',
        #     category=self.category2,
        #     brand=self.brand2,
        #     is_active=False,
        # )
        # self.product2.tags.add(self.tag2)
        # self.product_image1 = ProductImage.objects.create(
        #     product=self.product1,
        #     alt_text='Nike Skirt',
        #     is_active=True,
        # )
        # self.product_image2 = ProductImage.objects.create(
        #     product=self.product2,
        #     alt_text='Adidas Shirt',
        #     is_active=False,
        # )
        # self.product_attribute1 = ProductAttribute.objects.create(
        #     name='color',
        #     description='color'
        # )
        # self.product_attribute2 = ProductAttribute.objects.create(
        #     name='women clothing size',
        #     description='women clothing size'
        # )
        # self.product_type1 = ProductType.objects.create(
        #     name='women clothes',
        #     slug='women-clothes',
        #     description='women clothes'
        # )
        # self.product_type1.product_type_attributes.add(
        #     self.product_attribute1
        # )
        # self.product_type2 = ProductType.objects.create(
        #     name='men clothes',
        #     slug='men-clothes',
        #     description='men clothes'
        # )
        # self.product_type2.product_type_attributes.add(
        #     self.product_attribute2
        # )
        # self.product_attr_value1 = ProductAttributeValue.objects.create(
        #     product_attribute = self.product_attribute1,
        #     attribute_value = 'red'
        # )
        # self.product_attr_value2 = ProductAttributeValue.objects.create(
        #     product_attribute = self.product_attribute2,
        #     attribute_value = 'xs'
        # )
        # self.product_inventory1 = ProductInventory.objects.create(
        #     sku='11111',
        #     upc='11111',
        #     product=self.product1,
        #     product_type=self.product_type1,
        #     retail_price=10.00,
        #     store_price=11.00,
        #     sale_price=9.00,
        #     weight=float(1.0),
        #     is_active=True,
        # )
        # product_attr_value1 = ProductAttributeValue.objects.get(id=1)
        # product_attr_value2 = ProductAttributeValue.objects.get(id=2)
        # self.product_inventory1.attribute_values.set(
        #     [product_attr_value1, product_attr_value2],
        # )
        # self.product_inventory2 = ProductInventory.objects.create(
        #     sku='22222',
        #     upc='22222',
        #     product=self.product2,
        #     product_type=self.product_type1,
        #     retail_price=10.00,
        #     store_price=11.00,
        #     sale_price=9.00,
        #     weight=float(1.0),
        #     is_active=False,
        # )
        # self.product_inventory2.attribute_values.set(
        #     [product_attr_value1],
        # )
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
        # self.promotion.products_inventory_in_promotion.add(
        #     self.product_inventory1
        # )
        # urls
        self.client = Client()
        self.promotions_list_url = reverse('promotions_list')


    def test_promotions_list_view_status_code(self):
        """Test the status code for the promotions list view."""
        response = self.client.get(self.promotions_list_url)
        self.assertEquals(response.status_code, 200)

    def test_promotions_list_view_template_used(self):
        """Test the template used for the promotions list view."""
        response = self.client.get(self.promotions_list_url)
        self.assertTemplateUsed(response, 'account/login.html')
        # costumer login
        self.client.force_login(self.user)
        response = self.client.get(self.promotions_list_url)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()
        # manager login
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.promotions_list_url)
        self.assertEqual(response.context['promotions'].count(), 1)
        self.assertTemplateUsed(response, 'promotions/promotions_list.html')
        self.client.logout()