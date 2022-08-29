"""Tests for the models in the inventory app."""
from django.test import TestCase
from datetime import datetime, timedelta
from django.core import mail
from django.contrib.auth.models import User
from orders.models import Order, OrderItem
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
from email_notifications.models import StockEmailNotification
import cloudinary
import cloudinary.uploader
from reviews.models import Review, ReviewImage


class TestModels(TestCase):
    """Tests for the models in the inventory app."""

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
        self.stock1 = Stock.objects.create(
            product_inventory=self.product_inventory1,
            units=10,
            units_variable=10,
            units_sold=0,
        )
        self.stock2 = Stock.objects.create(
            product_inventory=self.product_inventory2,
            units=0,
            units_variable=10,
            units_sold=0,
        )

    def test_category_name(self):
        """Test the name field."""
        self.assertEqual(self.category1.name, 'Clothing')
        self.assertEqual(self.category1.slug, 'clothing')

    def test_category_is_active(self):
        """Test category is active."""
        self.assertEqual(self.category1.is_active, False)
        self.assertEqual(self.category2.is_active, True)

    def test_category_str(self):
        """Test category string representation."""
        self.assertEqual(str(self.category1), 'Clothing')
        self.assertEqual(str(self.category2), 'Food')

    def test_get_active_categories(self):
        """Test get_active_categories method."""
        self.assertQuerysetEqual(
            Category.get_active_categories(),
            [self.category2]
        )

    def test_get_not_active_categories(self):
        """Test get_not_active_categories method."""
        self.assertQuerysetEqual(
            Category.get_not_active_categories(),
            [self.category1]
        )

    def test_tag_name(self):
        """Test the name field."""
        self.assertEqual(self.tag1.name, 'skirt')
        self.assertEqual(self.tag1.slug, 'skirt')

    def test_tag_is_active(self):
        """Test tag is active."""
        self.assertEqual(self.tag1.is_active, True)
        self.assertEqual(self.tag2.is_active, False)

    def test_tag_str(self):
        """Test tag string representation."""
        self.assertEqual(str(self.tag1), 'skirt')
        self.assertEqual(str(self.tag2), 'shirt')

    def test_get_active_tags(self):
        """Test get_active_tags method."""
        self.assertQuerysetEqual(
            Tag.get_active_tags(),
            [self.tag1]
        )

    def test_get_not_active_tags(self):
        """Test get_not_active_tags method."""
        self.assertQuerysetEqual(
            Tag.get_not_active_tags(),
            [self.tag2]
        )

    def test_brand_name(self):
        """Test the name field."""
        self.assertEqual(self.brand1.name, 'Nike')
        self.assertEqual(self.brand1.slug, 'nike')

    def test_brand_is_active(self):
        """Test brand is active."""
        self.assertEqual(self.brand1.is_active, True)
        self.assertEqual(self.brand2.is_active, False)

    def test_brand_str(self):
        """Test brand string representation."""
        self.assertEqual(str(self.brand1), 'Nike')
        self.assertEqual(str(self.brand2), 'Adidas')

    def test_get_active_brands(self):
        """Test get_active_brands method."""
        self.assertQuerysetEqual(
            Brand.get_active_brands(),
            [self.brand1]
        )

    def test_get_not_active_brands(self):
        """Test get_not_active_brands method."""
        self.assertQuerysetEqual(
            Brand.get_not_active_brands(),
            [self.brand2]
        )

    def test_product_name(self):
        """Test the name field."""
        self.assertEqual(self.product1.name, 'Nike Skirt')
        self.assertEqual(self.product1.slug, 'nike-skirt')

    def test_product_description(self):
        """Test the description field."""
        self.assertEqual(self.product1.description, 'Nike Skirt')
        self.assertEqual(self.product2.description, 'Adidas Shirt')

    def test_product_category(self):
        """Test the category field."""
        self.assertEqual(self.product1.category, self.category1)
        self.assertEqual(self.product2.category, self.category2)

    def test_product_tags(self):
        """Test the tags field."""
        self.assertQuerysetEqual(self.product1.tags.all(), [self.tag1])
        self.assertQuerysetEqual(self.product2.tags.all(), [self.tag2])

    def test_product_brand(self):
        """Test the brand field."""
        self.assertEqual(self.product1.brand, self.brand1)
        self.assertEqual(self.product2.brand, self.brand2)

    def test_product_is_active(self):
        """Test product is active."""
        self.assertEqual(self.product1.is_active, True)
        self.assertEqual(self.product2.is_active, False)

    def test_product_str(self):
        """Test product string representation."""
        self.assertEqual(str(self.product1), 'Nike Skirt')
        self.assertEqual(str(self.product2), 'Adidas Shirt')

    def test_get_active_products(self):
        """Test get_active_products method."""
        self.assertQuerysetEqual(
            Product.get_active_products(),
            [self.product1]
        )

    def test_get_not_active_products(self):
        """Test get_not_active_products method."""
        self.assertQuerysetEqual(
            Product.get_not_active_products(),
            [self.product2]
        )

    def test_get_recently_created_products(self):
        """Test get_recently_created_products method."""
        self.assertTrue(
            self.product1.get_recently_created(),
            True
        )

    def test_get_tags_for_product(self):
        """Test get_tags_for_product method."""
        self.assertQuerysetEqual(
            Product.get_tags(self.product1),
            [self.tag1]
        )
        self.assertQuerysetEqual(
            Product.get_tags(self.product2),
            [self.tag2]
        )

    def test_product_get_main_image(self):
        """Test get_main_image method."""
        self.product_image1.default_image = True
        self.product_image1.save()
        self.assertEqual(self.product1.images.count(), 1)
        self.assertEqual(self.product_image1.default_image, True)
        product1 = Product.objects.get(id=self.product1.id)
        self.assertEqual(
            product1.get_main_image(),
            self.product_image1.image_url
        )
        self.product_image3 = ProductImage.objects.create(
            product=self.product1,
            alt_text='Nike Skirt',
            image=None,
            default_image=True
        )
        self.assertEqual(self.product_image3.default_image, True)
        self.assertEqual(self.product_image2.default_image, False)
        self.assertEqual(self.product1.images.count(), 2)
        self.assertEqual(
            product1.get_main_image(),
            self.product_image3.image_url
        )
        self.product_image1.default_image = False
        self.product_image1.is_active = False
        self.product_image1.save()
        self.product_image3.default_image = False
        self.product_image3.is_active = False
        self.product_image3.save()
        self.assertEqual(
            product1.get_main_image(),
            (
                'https://res.cloudinary.com/learning-coding/image/uploa' +
                'd/v1656240479/default_product_image.png'
            )
        )
        self.product_image1.delete()
        self.product_image3.delete()
        self.assertEqual(
            product1.get_main_image(),
            (
                'https://res.cloudinary.com/learning-coding/image/uploa' +
                'd/v1656240479/default_product_image.png'
            )
        )

    def test_product_get_out_of_stock(self):
        """Test get_out_of_stock method."""
        self.assertEqual(self.product1.get_out_of_stock(), False)
        self.product_inventory1.is_active = False
        self.product_inventory1.save()
        self.assertEqual(self.product1.get_out_of_stock(), True)

    def test_product_get_same_price(self):
        """Test get_same_price method."""
        self.assertEqual(self.product1.get_same_sale_price(), True)
        self.product_inventory3 = ProductInventory.objects.create(
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
        product_attr_value1 = ProductAttributeValue.objects.get(id=1)
        product_attr_value2 = ProductAttributeValue.objects.get(id=2)
        self.product_inventory3.attribute_values.set(
            [product_attr_value1, product_attr_value2],
        )
        self.assertEqual(self.product1.get_same_sale_price(), True)
        self.product_inventory1.sale_price = 11.00
        self.product_inventory1.save()
        self.assertEqual(self.product1.get_same_sale_price(), False)
        self.product_inventory3.sale_price = 11.00
        self.product_inventory3.save()
        self.assertEqual(self.product1.get_same_sale_price(), True)
        self.product_inventory1.is_active = False
        self.product_inventory1.save()
        self.product_inventory3.is_active = False
        self.product_inventory3.save()
        self.assertEqual(self.product1.get_same_sale_price(), False)

    def test_product_get_sale_price_is_lower_than_store_price(self):
        """Test get_sale_price_is_lower_than_store_price method."""
        self.assertEqual(
            self.product1.get_sale_price_is_lower_than_store_price(),
            True
        )
        self.product_inventory1.sale_price = 11.00
        self.product_inventory1.save()
        self.assertEqual(
            self.product1.get_sale_price_is_lower_than_store_price(),
            False
        )
        self.product_inventory1.is_active = False
        self.product_inventory1.save()
        self.assertEqual(
            self.product1.get_sale_price_is_lower_than_store_price(),
            False
        )

    def test_product_get_lowest_price(self):
        """Test get_lowest_price method."""
        self.assertEqual(self.product1.get_lowest_price(), 9.00)
        self.product_inventory3 = ProductInventory.objects.create(
            sku='11112',
            upc='11112',
            product=self.product1,
            product_type=self.product_type1,
            retail_price=10.00,
            store_price=11.00,
            sale_price=8.00,
            weight=float(1.0),
            is_active=True,
        )
        product_attr_value1 = ProductAttributeValue.objects.get(id=1)
        product_attr_value2 = ProductAttributeValue.objects.get(id=2)
        self.product_inventory3.attribute_values.set(
            [product_attr_value1, product_attr_value2],
        )
        self.assertEqual(self.product1.get_lowest_price(), 8.00)
        self.product_inventory1.is_active = False
        self.product_inventory1.save()
        self.product_inventory3.is_active = False
        self.product_inventory3.save()
        self.assertEqual(self.product1.get_lowest_price(), None)

    def test_product_get_highest_price(self):
        """Test get_highest_price method."""
        self.assertEqual(self.product1.get_highest_price(), 9.00)
        self.product_inventory3 = ProductInventory.objects.create(
            sku='11112',
            upc='11112',
            product=self.product1,
            product_type=self.product_type1,
            retail_price=10.00,
            store_price=11.00,
            sale_price=11.00,
            weight=float(1.0),
            is_active=True,
        )
        product_attr_value1 = ProductAttributeValue.objects.get(id=1)
        product_attr_value2 = ProductAttributeValue.objects.get(id=2)
        self.product_inventory3.attribute_values.set(
            [product_attr_value1, product_attr_value2],
        )
        self.assertEqual(self.product1.get_highest_price(), 11.00)
        self.product_inventory1.is_active = False
        self.product_inventory1.save()
        self.product_inventory3.is_active = False
        self.product_inventory3.save()
        self.assertEqual(self.product1.get_highest_price(), None)

    def test_product_get_lowest_store_price(self):
        """Test get_lowest_price method."""
        self.assertEqual(self.product1.get_lowest_store_price(), 11.00)
        self.product_inventory3 = ProductInventory.objects.create(
            sku='11112',
            upc='11112',
            product=self.product1,
            product_type=self.product_type1,
            retail_price=10.00,
            store_price=9.00,
            sale_price=8.00,
            weight=float(1.0),
            is_active=True,
        )
        product_attr_value1 = ProductAttributeValue.objects.get(id=1)
        product_attr_value2 = ProductAttributeValue.objects.get(id=2)
        self.product_inventory3.attribute_values.set(
            [product_attr_value1, product_attr_value2],
        )
        self.assertEqual(self.product1.get_lowest_store_price(), 9.00)
        self.product_inventory1.is_active = False
        self.product_inventory1.save()
        self.product_inventory3.is_active = False
        self.product_inventory3.save()
        self.assertEqual(self.product1.get_lowest_store_price(), None)

    def test_product_get_highest_store_price(self):
        """Test get_highest_price method."""
        self.assertEqual(self.product1.get_highest_store_price(), 11.00)
        self.product_inventory3 = ProductInventory.objects.create(
            sku='11112',
            upc='11112',
            product=self.product1,
            product_type=self.product_type1,
            retail_price=10.00,
            store_price=13.00,
            sale_price=11.00,
            weight=float(1.0),
            is_active=True,
        )
        product_attr_value1 = ProductAttributeValue.objects.get(id=1)
        product_attr_value2 = ProductAttributeValue.objects.get(id=2)
        self.product_inventory3.attribute_values.set(
            [product_attr_value1, product_attr_value2],
        )
        self.assertEqual(self.product1.get_highest_store_price(), 13.00)
        self.product_inventory1.is_active = False
        self.product_inventory1.save()
        self.product_inventory3.is_active = False
        self.product_inventory3.save()
        self.assertEqual(self.product1.get_highest_store_price(), None)

    def test_product_image_name(self):
        """Test the name field."""
        self.assertEqual(self.product_image1.alt_text, 'Nike Skirt')

    def test_product_image_product(self):
        """Test the product field."""
        self.assertEqual(self.product_image1.product, self.product1)

    def test_product_image_image(self):
        """Test the image field."""
        self.assertEqual(self.product_image1.image, None)

    def test_product_image_default_image(self):
        """Test the default_image field."""
        self.product_image1.default_image = True
        self.product_image1.save()
        self.assertEqual(self.product1.images.count(), 1)
        self.assertEqual(self.product_image1.default_image, True)
        self.product_image3 = ProductImage.objects.create(
            product=self.product1,
            alt_text='Nike Skirt',
            image=None,
            default_image=True
        )
        self.assertEqual(self.product_image3.default_image, True)
        self.assertEqual(self.product_image2.default_image, False)
        self.assertEqual(self.product1.images.count(), 2)

    def test_product_image_is_active(self):
        """Test product image is active."""
        self.assertEqual(self.product_image1.is_active, True)
        self.assertEqual(self.product_image2.is_active, False)

    def test_product_image_str(self):
        """Test product image string representation."""
        self.assertEqual(str(self.product_image1), 'Nike Skirt')
        self.assertEqual(str(self.product_image2), 'Adidas Shirt')

    def test_product_image_url(self):
        """Test product image url."""
        image1 = ProductImage.objects.get(id=1)
        self.assertEqual(
            image1.image_url,
            'static/images/default_product_image.png'
        )
        image1.image = cloudinary.uploader.upload_image(
            'static/images/test_product_image.png'
        )
        image1.save()
        self.assertTrue(
          'res.cloudinary.com' in image1.image_url
        )

    def test_get_active_product_images(self):
        """Test get_active_product_images method."""
        self.assertQuerysetEqual(
            ProductImage.get_active_product_images(),
            [self.product_image1]
        )

    def test_get_not_active_product_images(self):
        """Test get_not_active_product_images method."""
        self.assertQuerysetEqual(
            ProductImage.get_not_active_product_images(),
            [self.product_image2]
        )

    def test_product_attribute_name(self):
        """Test the name field."""
        self.assertEqual(self.product_attribute1.name, 'color')
        self.assertEqual(
            self.product_attribute2.name,
            'women clothing size'
        )

    def test_product_attribute_str(self):
        """Test string method"""
        self.assertEqual(str(self.product_attribute1), 'color')

    def test_product_type_name(self):
        """Test the name field."""
        self.assertEqual(self.product_type1.name, 'women clothes')
        self.assertEqual(self.product_type1.slug, 'women-clothes')

    def test_product_type_str(self):
        """Test string method"""
        self.assertEqual(str(self.product_type1), 'women clothes')

    def test_get_product_type_attributes(self):
        """Test get product type attributes method"""
        self.assertQuerysetEqual(
            ProductType.get_product_type_attributes(self.product_type1),
            [self.product_attribute1]
        )

    def test_product_attribute_value_name(self):
        """Test the name field"""
        self.assertEqual(self.product_attr_value1.attribute_value, 'red')

    def test_product_attribute_value_str(self):
        """Test string method"""
        self.assertEqual(str(self.product_attr_value1), 'red')

    def test_product_inventory_attribute_values_field(self):
        """Test the attribute values field"""
        self.assertEqual(self.product_inventory1.sku, '11111')
        self.assertEqual(self.product_inventory1.upc, '11111')
        self.assertEqual(
            str(self.product_inventory1.product),
            'Nike Skirt'
        )
        self.assertEqual(
            str(self.product_inventory1.product_type),
            'women clothes'
        )
        self.assertQuerysetEqual(
            self.product_inventory1.attribute_values.all(),
            [self.product_attr_value1, self.product_attr_value2]
        )

    def test_product_inventory_attribute_values_str(self):
        """Test string method"""
        self.assertEqual(
            str(self.product_inventory1),
            '11111 - 11111'
        )

    def test_get_all_attribute_values_str(self):
        """Test get all attribute values str method"""
        self.assertEqual(
            str(self.product_inventory1.get_all_attribute_values_str()),
            'color: red women clothing size: xs '
        )

    def test_get_active_product_inventory(self):
        """Test get_active_product_images method."""
        self.assertQuerysetEqual(
            ProductInventory.get_active_product_inventories(),
            [self.product_inventory1]
        )

    def test_get_not_active_product_inventory(self):
        """Test get_not_active_product_inventory method."""
        self.assertQuerysetEqual(
            ProductInventory.get_not_active_product_inventories(),
            [self.product_inventory2]
        )

    def test_get_attribute_values(self):
        """Test get_attribute_values method"""
        self.assertQuerysetEqual(
            ProductInventory.get_attribute_values(self.product_inventory1),
            [self.product_attr_value1, self.product_attr_value2]
        )

    def test_stock_status_str(self):
        """Test the name field."""
        self.assertEqual(str(self.stock1), '11111 - 10')
        self.assertEqual(str(self.stock2), '22222 - Out of stock')
        # count product inventories
        self.assertEqual(ProductInventory.objects.count(), 2)
        self.product_inventory3 = ProductInventory.objects.create(
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
        self.assertEqual(ProductInventory.objects.count(), 3)
        # create stock with product inventory is null
        stock3 = Stock.objects.create(
            product_inventory=self.product_inventory3,
            units=10,
            units_variable=10,
            units_sold=0,
        )
        # delete product inventory3
        self.product_inventory3.delete()
        # count product inventories
        self.assertEqual(ProductInventory.objects.count(), 2)

    def test_reset_product_inventory_is_active(self):
        """Test reset_product_inventory_is_active method."""
        self.assertEqual(self.product_inventory1.is_active, True)
        self.assertEqual(self.product_inventory2.is_active, False)
        self.stock1.units = 0
        self.stock1.save()
        self.assertEqual(self.product_inventory1.is_active, False)
        self.assertEqual(self.product_inventory2.is_active, False)

    def test_email_sent_to_user(self):
        """Test email sent to user."""
        self.assertEqual(len(mail.outbox), 0)
        self.stock1.units = 5
        self.stock1.save()
        self.assertEqual(len(mail.outbox), 0)
        stock_email_notification = StockEmailNotification.objects.create(
            user=self.user,
            requested_product=self.product1,
            requested_quantity=50,
            answer_sent=False
        )
        stock_email_notification2 = StockEmailNotification.objects.create(
            user=self.user2,
            requested_product=self.product1,
            requested_quantity=20,
            answer_sent=True
        )
        stock_email_notification3 = StockEmailNotification.objects.create(
            user=self.user3,
            requested_product=self.product1,
            requested_quantity=100,
            answer_sent=False
        )
        stock_email_notification.save()
        self.assertEqual(len(mail.outbox), 4)
        stock_email_notification2.save()
        self.assertEqual(len(mail.outbox), 5)
        stock_email_notification3.save()
        self.assertEqual(len(mail.outbox), 6)
        self.assertEqual(
            stock_email_notification.
            get_all_requested_attributes_values_objects(), ''
        )
        stock_email_notification.requested_attributes_values.add(
          self.product_attr_value1
        )
        stock_email_notification.requested_attributes_values.add(
          self.product_attr_value2
        )
        stock_email_notification2.requested_attributes_values.add(
          self.product_attr_value1
        )
        self.stock1.units = 50
        self.stock1.save()
        self.assertEqual(len(mail.outbox), 8)

    def test_get_high_sales_fewer_products(self):
        """Test get_high_sales method."""
        self.stock1.units = 1
        self.stock1.units_sold = 2
        self.stock1.save()
        self.assertQuerysetEqual(
            self.stock1.get_high_sales_fewer_products(),
            [self.stock1]
        )

    def test_get_units_inconsistent(self):
        """Test get_units_inconsistent method."""
        self.stock1.save()
        self.assertQuerysetEqual(
            self.stock1.get_units_inconsistent(),
            [self.stock2]
        )

    def test_get_low_stock_50(self):
        """Test get_low_stock_50 method."""
        self.stock1.units = 60
        self.stock1.save()
        self.assertQuerysetEqual(
            self.stock1.get_low_stock_50(),
            [self.stock2]
        )
        self.stock1.units = 50
        self.stock1.save()
        self.assertQuerysetEqual(
            self.stock1.get_low_stock_50(),
            [self.stock1, self.stock2]
        )

    def test_get_low_stock_20(self):
        """Test get_low_stock_20 method."""
        self.stock1.units = 60
        self.stock1.save()
        self.assertQuerysetEqual(
            self.stock1.get_low_stock_20(),
            [self.stock2]
        )
        self.stock1.units = 20
        self.stock1.save()
        self.assertQuerysetEqual(
            self.stock1.get_low_stock_20(),
            [self.stock1, self.stock2]
        )

    def test_get_low_stock_10(self):
        """Test get_low_stock_10 method."""
        self.stock1.units = 60
        self.stock1.save()
        self.assertQuerysetEqual(
            self.stock1.get_low_stock_10(),
            [self.stock2]
        )
        self.stock1.units = 10
        self.stock1.save()
        self.assertQuerysetEqual(
            self.stock1.get_low_stock_10(),
            [self.stock1, self.stock2]
        )

    def test_get_out_of_stock(self):
        """Test get_out_of_stock method."""
        self.stock1.units = 60
        self.stock1.save()
        self.assertQuerysetEqual(
            self.stock1.get_out_of_stock(),
            [self.stock2]
        )
        self.stock1.units = 0
        self.stock1.save()
        self.assertQuerysetEqual(
            self.stock1.get_out_of_stock(),
            [self.stock1, self.stock2]
        )

    def test_get_low_sales(self):
        """Test get_low_sales method."""
        self.stock1.units = 500
        self.stock1.units_sold = 2
        self.stock1.save()
        self.assertQuerysetEqual(
            self.stock1.get_low_sales(),
            [self.stock1]
        )

    def test_product_attribute_values_unique_together(self):
        """Test the unique together constraint."""
        product_attr_value3 = ProductAttributeValue.objects.create(
            product_attribute=self.product_attribute1,
            attribute_value='yellow',
        )
        attributevalues = ProductAttributeValue.objects.get(
            id=product_attr_value3.id
        )
        productinventory = ProductInventory.objects.get(
            id=self.product_inventory2.id
        )
        original = ProductAttributeValues.objects.create(
            attributevalues=attributevalues,
            productinventory=productinventory
        )
        self.assertNotEquals(original, None)
        with self.assertRaises(Exception):
            original_clone = ProductAttributeValues.objects.create(
                attributevalues=attributevalues,
                productinventory=productinventory
            )

    def test_product_type_attribute_unique_together(self):
        """Test the unique together constraint."""
        product_attribute3 = ProductAttribute.objects.create(
            name='toys size',
            description='toys size'
        )
        product_type3 = ProductType.objects.create(
            name='toys',
            slug='toys',
            description='toys'
        )
        product_attribute = ProductAttribute.objects.get(
            id=product_attribute3.id
        )
        product_type = ProductType.objects.get(
            id=product_type3.id
        )
        original = ProductTypeAttribute.objects.create(
            product_attribute=product_attribute,
            product_type=product_type
        )
        self.assertNotEquals(original, None)
        with self.assertRaises(Exception):
            original_clone = ProductTypeAttribute.objects.create(
                product_attribute=product_attribute,
                product_type=product_type
            )

    def test_get_average_rating(self):
        """Test average rating for and image"""
        self.assertEqual(self.product1.get_average_rating(), 0)
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
        self.assertEqual(self.product1.get_average_rating(), 5)
