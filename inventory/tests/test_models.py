"""Tests for the models in the inventory app."""
from django.test import TestCase
from inventory.models import Category
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