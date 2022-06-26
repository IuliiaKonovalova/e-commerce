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

    def test_add_remove_product_wishlist_ajax_url(self):
        """Test add remove product wishlist AJAX url."""
        url = reverse('add_remove_product_wishlist_ajax')
        self.assertEquals(
            resolve(url).func.view_class, AddRemoveProductWishlistAJAXView
        )

    def test_empty_wishlist_ajax_url(self):
        """Test empty wishlist AJAX url."""
        url = reverse('empty_wishlist_ajax')
        self.assertEquals(
            resolve(url).func.view_class,
            EmptyWishlistAJAXView
        )
