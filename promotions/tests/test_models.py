"""Tests for the Promotion model."""
from django.test import TestCase
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
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


class PromotionTestCase(TestCase):
    """Test case for the Promotion model."""
    def setUp(self):
        """Set up the test case."""
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
        self.promotion.products_inventory_in_promotion.add(
            self.product_inventory1
        )

    def test_str(self):
        """Test the __str__ method."""
        self.assertEqual(
            str(self.promotion),
            'Promotion 1'
        )

    def test_get_promotion_code(self):
        """Test the get_promotion_code method."""
        self.assertEqual(
            self.promotion.get_promotion_code(),
            'PROMO1'
        )

    def test_is_active_now(self):
        """Test the is_active_now method."""
        self.assertTrue(
            self.promotion.is_active_now()
        )
        self.promotion.active = False
        self.promotion.save()
        self.assertFalse(
            self.promotion.is_active_now()
        )

    def test_is_active_soon(self):
        """Test the is_active_soon method."""
        self.assertTrue(
            self.promotion.is_active_soon()
        )
        self.promotion.active = False
        self.promotion.save()
        self.assertFalse(
            self.promotion.is_active_soon()
        )
        promotion2 = Promotion.objects.create(
            name='Promotion 2',
            slug='promotion-2',
            description='Promotion 2 description',
            promotion_code='PROMO2',
            promotion_reduction=10,
            start_date=datetime.now() + timezone.timedelta(days=1),
            end_date=datetime.now() + timezone.timedelta(days=365 * 5),
            active=True,
        )
        promotion2.products_inventory_in_promotion.add(
            self.product_inventory1
        )
        self.assertTrue(
            promotion2.is_active_soon()
        )
        promotion3 = Promotion.objects.create(
            name='Promotion 3',
            slug='promotion-3',
            description='Promotion 3 description',
            promotion_code='PROMO3',
            promotion_reduction=10,
            start_date=datetime.now() + timezone.timedelta(days=10),
            end_date=datetime.now() + timezone.timedelta(days=365 * 5),
            active=True,
        )
        promotion3.products_inventory_in_promotion.add(
            self.product_inventory1
        )
        self.assertFalse(
            promotion3.is_active_soon()
        )

    def test_get_products_in_promotion(self):
        """Test the get_products_in_promotion method."""
        self.assertEqual(
            self.promotion.get_products_in_promotion()[0],
            self.product_inventory1
        )
