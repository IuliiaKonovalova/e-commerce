"""Test Bag views."""
from django.test import TestCase, Client
from django.urls import reverse


class TestBagViews(TestCase):
    """Test Bag views."""

    def setUp(self):
        """Set up the test."""
        self.client = Client()
        self.user = self.client.login(
            username='testuser',
            password='testpassword'
        )

    def test_bag_display_view(self):
        """Test bag display view."""
        response = self.client.get(reverse('bag_display'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag_display.html')