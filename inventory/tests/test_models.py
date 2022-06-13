"""Tests for the models in the inventory app."""
from django.test import TestCase
from inventory.models import (
    Category,
    Tag,
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

    def test_tag_name(self):
        """Test the name field."""
        self.assertEqual(self.tag1.name, 'skirt')
        self.assertEqual(self.tag1.slug, 'skirt')

    def test_tag_slug(self):
        """Test tag slug."""
        self.assertEqual(self.tag1.slug, 'skirt')
        self.assertEqual(self.tag2.slug, 'shirt')

    def test_tag_is_active(self):
        """Test tag is active."""
        self.assertEqual(self.tag1.is_active, True)
        self.assertEqual(self.tag2.is_active, False)

    def test_tag_str(self):
        """Test tag string representation."""
        self.assertEqual(str(self.tag1), 'skirt')
        self.assertEqual(str(self.tag2), 'shirt')
