"""Test Bag URLs."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from bag.views import (
    BagDisplayView,
    AddToBagAJAXView,
)


class TestUrls(SimpleTestCase):
    """Test Bag URLs."""

    def test_bag_display_url(self):
        """Test bag display url."""
        url = reverse('bag_display')
        self.assertEquals(resolve(url).func.view_class, BagDisplayView)

    def test_add_to_bag_url(self):
        """Test add to bag url."""
        url = reverse('add_to_bag')
        self.assertEquals(resolve(url).func.view_class, AddToBagAJAXView)