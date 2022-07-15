"""Tests for Reviews models."""
from django.test import TestCase
from django.contrib.auth.models import User
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
from orders.models import Order, OrderItem
from profiles.models import Role
from reviews.models import Review, ReviewImage
import cloudinary
import cloudinary.uploader


class TestReview(TestCase):
    """Tests for Review models."""

    def setUp(self):
        """Set up for tests."""
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
        # create order
        self.order1 = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@gmail.com',
            phone='1234567890',
            address1='123 Main St',
            address2='',
            city='New York',
            county_region_state='NY',
            country='USA',
            zip_code='10001',
            total_paid=10.00,
            order_number='',
            order_key='4rguytrfdre454tgETreyhtgfgsd',
            billing_status=False,
            status='Pending',
        )
        self.order1.save()
        self.get_order_number = Order.objects.get(id=1).order_number
        self.order_item1 = OrderItem.objects.create(
            order=self.order1,
            product_inventory=self.product_inventory1,
            quantity=1,
        )
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

    def test_review_model(self):
        """Tests for Review model str."""
        self.assertEqual(str(self.review1), 'testuser - Nike Skirt - 5')

    def test_review_model_image(self):
        """Tests for Review model image."""
        self.assertEqual(str(self.review_image1), 'testuser - Nike Skirt')

    def test_review_image_url(self):
        """Tests for Review image url."""
        image1 = ReviewImage.objects.get(id=1)
        self.assertEqual(
            image1.image_url,
            False
        )
        image1.image = cloudinary.uploader.upload_image(
            'static/images/test_product_image.png'
        )
        image1.save()
        self.assertTrue(
          'res.cloudinary.com' in image1.image_url
        )
