"""Test forms for orders app"""
from django.test import TestCase
from django.urls import reverse
from orders.forms import OrderForm


class OrderFormTest(TestCase):
    """Test case for the Order model."""
    def test_order_has_fields(self):
        """Test order form has expected fields."""
        expected = [
            'full_name',
            'email',
            'phone',
            'address1',
            'address2',
            'city',
            'county_region_state',
            'country',
            'zip_code',
            'total_paid',
            'billing_status',
            'status',
        ]
        actual = list(OrderForm().fields)
        self.assertListEqual(expected, actual)

    def test_order_form_is_valid(self):
        """Test order form is valid."""
        form = OrderForm({
            'full_name': 'Test Order',
            'email': 'test@mail.com',
            'phone': '1234567890',
            'address1': 'Test Address 1',
            'address2': 'Test Address 2',
            'city': 'Test City',
            'county_region_state': 'Test County',
            'country': 'Test Country',
            'zip_code': '12345',
            'total_paid': 10,
            'billing_status': True,
            'status': 'Test Status',
        })
        self.assertTrue(form.is_valid())

    def test_order_form_is_invalid(self):
        """Test order form is invalid."""
        form = OrderForm({
            'full_name': '',
            'email': '',
            'phone': '',
            'address1': '',
            'address2': '',
            'city': '',
            'county_region_state': '',
            'country': '',
            'zip_code': '',
            'total_paid': '',
            'billing_status': '',
            'status': '',
        })
        self.assertFalse(form.is_valid())
