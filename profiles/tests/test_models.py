"""Tests for the models of the profiles app."""
from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Roles


class TestModels(TestCase):
    """Tests for the Roles model."""

    def setUp(self):
        """Set up the test."""
        self.role = Roles.objects.create(
            name='Test role',
            description='Test description'
        )

    def test_role_name(self):
        """Test the name field."""
        self.assertEqual(self.role.name, 'Test role')
        self.assertEqual(self.role.description, 'Test description')
