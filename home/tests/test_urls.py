"""Test for Home Urls"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from home.views import HomeView


class TestUrls(SimpleTestCase):
    """Test for Home Urls"""

    def test_home_url(self):
        """Test for Home Urls"""
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, HomeView)
