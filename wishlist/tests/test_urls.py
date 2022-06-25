"""Test Wishlist URLs."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from wishlist.views import (
    WishlistDisplayView,
    AddRemoveProductWishlistAJAXView,
    EmptyWishlistAJAXView,
)


class TestUrls(SimpleTestCase):
    """Test Wishlist URLs."""

    def test_wishlist_display_url(self):
        """Test wishlist display url."""
        url = reverse('wishlist_display')
        self.assertEquals(resolve(url).func.view_class, WishlistDisplayView)


