"""Test Bag URLs."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from bag.views import (
    BagDisplayView,
)


class TestUrls(SimpleTestCase):
    """Test Bag URLs."""

    def test_bag_display_url(self):
        """Test bag display url."""
        url = reverse('bag_display')
        self.assertEquals(resolve(url).func.view_class, BagDisplayView)