"""Tests for the models in the inventory app."""
from django.test import TestCase
from inventory.models import (
    Category,
    Tag,
    Brand,
    Product,
    ProductImage,
)
import cloudinary
import cloudinary.uploader


class TestModels(TestCase):
    """Tests for the models in the inventory app."""

    def setUp(self):
        """Set up the test."""
        self.category1 = Category.objects.create(
            name='Clothing',
            slug='Clothing',
            is_active=False,
        )
        self.category2 = Category.objects.create(
            name='Food',
            slug='Food',
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
            slug='Nike',
            is_active=True,
        )
        self.brand2 = Brand.objects.create(
            name='Adidas',
            slug='Adidas',
            is_active=False,
        )
        self.product1 = Product.objects.create(
            name='Nike Skirt',
            slug='Nike-Skirt',
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

    def test_category_name(self):
        """Test the name field."""
        self.assertEqual(self.category1.name, 'Clothing')
        self.assertEqual(self.category1.slug, 'Clothing')

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
        self.assertEqual(self.brand1.slug, 'Nike')

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
        self.assertEqual(self.product1.slug, 'Nike-Skirt')

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

    def test_product_image_name(self):
        """Test the name field."""
        self.assertEqual(self.product_image1.alt_text, 'Nike Skirt')

    def test_product_image_product(self):
        """Test the product field."""
        self.assertEqual(self.product_image1.product, self.product1)

    def test_product_image_image(self):
        """Test the image field."""
        self.assertEqual(self.product_image1.image, None)

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
