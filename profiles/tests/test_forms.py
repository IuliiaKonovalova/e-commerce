"""Tests for the forms of the profile app."""
from django.test import TestCase
from django.contrib.auth.models import User
from profiles.forms import ProfileForm
from profiles.models import Role, Profile, Address
import cloudinary
import cloudinary.uploader


class TestForms(TestCase):
    """Tests for the forms of the profile app."""

    def setUp(self):
        """Set up the test."""
        self.role1 = Role.objects.create(
            name='Customer',
            description='Customer'
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
        self.address1 = Address.objects.create(
            user=self.user,
            country='USA',
            county_region='California',
            city='San Francisco',
            address_line='123 Main St',
            zip_code='12345',
            phone_number='1234567890',
            is_primary=False,
            created_at='2020-01-01',
            updated_at='2020-01-01'
        )

    def test_profile_form_has_fields(self):
        """Test the profile form has the correct fields."""
        form = ProfileForm()
        expected = ['first_name', 'last_name', 'birthday', 'avatar', 'subscription']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_profile_form(self):
        """Test the profile form."""
        form = ProfileForm(
            data={
                'first_name': 'Test',
                'last_name': 'User',
                'birthday': '2020-01-01',
                'avatar': '',
                'subscription': True
            }
        )
        self.assertTrue(form.is_valid())
