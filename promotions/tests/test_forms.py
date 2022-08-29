"""Tests for promotions app."""
from django.test import TestCase
from promotions.forms import PromotionForm


class PromotionTestCase(TestCase):
    """Test case for the Promotion model."""
    def test_promotion_form_has_fields(self):
        """Test promotion form has expected fields."""
        expected = [
            'name',
            'description',
            'promotion_code',
            'promotion_reduction',
            'start_date',
            'end_date',
            'products_inventory_in_promotion',
            'active',
        ]
        actual = list(PromotionForm().fields)
        self.assertListEqual(expected, actual)

    def test_promotion_form_is_valid(self):
        """Test promotion form is valid."""
        form = PromotionForm({
            'name': 'Test Promotion',
            'description': 'Test Promotion Description',
            'promotion_code': 'TESTPROMO',
            'promotion_reduction': 10,
            'active': True,
            'start_date': '2020-01-01',
            'end_date': '2020-01-01',
        })
        self.assertTrue(form.is_valid())

    def test_promotion_form_is_invalid(self):
        """Test promotion form is invalid."""
        form = PromotionForm({
            'name': '',
            'description': '',
            'promotion_code': '',
            'promotion_reduction': '',
            'active': '',
            'start_date': '',
            'end_date': '',
        })
        self.assertFalse(form.is_valid())
