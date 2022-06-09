"""Tests for the views of the profile app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import Role, Profile, Address
import cloudinary
import cloudinary.uploader


class TestViews(TestCase):
    """Tests for the Roles model."""

    def setUp(self):
        """Set up the test."""
        self.client = Client()
        self.user_profile_url = reverse('my_profile', kwargs={'user': 'testuser'})
        self.role1 = Role.objects.create(
            name='Customer',
            description='Customer'
        )
        self.role2 = Role.objects.create(
            name='Manager',
            description='Manager'
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

    def test_user_profile_view(self):
        """Test user profile view."""
        self.client.force_login(self.user)
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/my_profile.html')
        self.client.logout()
        response = self.client.get(self.user_profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')