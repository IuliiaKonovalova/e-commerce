"""Test Bag URLs."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from bag.views import (
    BagDisplayView,
    AddToBagAJAXView,
    RemoveUnitFromBagAJAXView,
    AddUnitToBagAJAXView,
    RemoveAllItemUnitsFromBagAJAXView,
    RemoveAllBagAJAXView,
    PromoCodeAJAXView,
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

    def test_add_unit_to_bag_url(self):
        """Test add unit to bag url."""
        url = reverse('add_unit_to_bag')
        self.assertEquals(
            resolve(url).func.view_class, AddUnitToBagAJAXView
        )

    def test_remove_all_item_units_from_bag_url(self):
        """Test remove all item units from bag url."""
        url = reverse('remove_all_item_units_from_bag')
        self.assertEquals(
            resolve(url).func.view_class, RemoveAllItemUnitsFromBagAJAXView
        )

    def test_remove_all_bag_url(self):
        """Test remove all bag url."""
        url = reverse('remove_all_bag')
        self.assertEquals(resolve(url).func.view_class, RemoveAllBagAJAXView)

    def test_apply_promo_code_url(self):
        """Test apply promo code url."""
        url = reverse('apply_promo_code')
        self.assertEquals(resolve(url).func.view_class, PromoCodeAJAXView)
