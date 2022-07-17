"""Tests for reviews views."""
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

class TestReviewsViews(TestCase):
    """Tests for reviews views."""
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
        # set order item
        self.order_item1 = OrderItem.objects.create(
            order=self.order1,
            product_inventory=self.product_inventory1,
            quantity=1,
        )
        self.order_item2 = OrderItem.objects.create(
            order=self.order1,
            product_inventory=self.product_inventory2,
            quantity=1,
        )
        # set review
        self.review1 = Review.objects.create(
            user=self.user,
            order=self.order1,
            product=self.product1,
            rating=5,
            comment='Good product',
        )
        self.review2 = Review.objects.create(
            user=self.user,
            order=self.order1,
            product=self.product2,
            rating=4,
            comment='Good product',
        )
        # set reviewImage
        self.reviewImage1 = ReviewImage.objects.create(
            review=self.review1,
            image=''
        )
        # image = open('static/images/test_product_image.png', 'rb')
        # self.reviewImage2 = ReviewImage.objects.create(
        #     review=self.review2,
        #     image=image
        # )
        # urls
        self.client = Client()
        self.review_url = reverse(
            'review',
            kwargs={'order_id': 1, 'product_id': 1}
        )
        self.add_review_url = reverse(
            'add_review',
            kwargs={'order_id': 1, 'product': 1}
        )

    def test_review_view(self):
        response = self.client.get(self.review_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_detail.html')

