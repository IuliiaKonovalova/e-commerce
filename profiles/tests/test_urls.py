"""Test Profiles URLs."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from profiles.views import (
    UserProfileView
)


class TestUrls(SimpleTestCase):
    """Test Profiles URLs."""

    def test_profile_url(self):
        """Test profile url."""
        url = reverse('my_profile', kwargs={'user': 'testuser'})
        self.assertEquals(resolve(url).func.view_class, UserProfileView)