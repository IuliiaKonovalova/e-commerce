"""Test Bag URLs."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from bag.views import (
    BagDisplayView,
    AddToBagAJAXView,
    RemoveUnitFromBagAJAXView,
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

    def test_remove_unit_from_bag_url(self):
        """Test remove unit from bag url."""
        url = reverse('remove_unit_from_bag')
        self.assertEquals(
            resolve(url).func.view_class, RemoveUnitFromBagAJAXView
        )
