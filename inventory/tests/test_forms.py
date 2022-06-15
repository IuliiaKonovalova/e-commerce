"""Tests for the forms of the inventory app."""
from django.test import TestCase
from inventory.forms import (
    CategoryForm,
    TagForm,
    BrandForm,
    ProductForm,
    ProductImageForm,
    ProductAttributeForm,
    # ProductTypeForm,
)


class TestForms(TestCase):
    """Tests for the forms of the inventory app."""
    def test_category_form_has_fields(self):
        """Test the category form has the correct fields."""
        form = CategoryForm()
        expected = ['name', 'slug', 'is_active']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_category_form_is_valid(self):
        """Test the category form is valid."""
        form = CategoryForm(
            data={
                'name': 'Test Category',
                'slug': 'test-category',
                'is_active': True
            }
        )
        self.assertTrue(form.is_valid())

    def test_category_form_is_invalid(self):
        """Test the category form is invalid."""
        form = CategoryForm(
            data={
                'name': 'Test Category',
                'slug': '',
                'is_active': True
            }
        )
        self.assertFalse(form.is_valid())


    def test_tag_form_has_fields(self):
        """Test the tag form has the correct fields."""
        form = TagForm()
        expected = ['name', 'slug', 'is_active']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_tag_form_is_valid(self):
        """Test the tag form is valid."""
        form = TagForm(
            data={
                'name': 'Test Tag',
                'slug': 'test-tag',
                'is_active': True
            }
        )
        self.assertTrue(form.is_valid())

    def test_tag_form_is_invalid(self):
        """Test the tag form is invalid."""
        form = TagForm(
            data={
                'name': 'Test Tag',
                'slug': '',
                'is_active': True
            }
        )
        self.assertFalse(form.is_valid())