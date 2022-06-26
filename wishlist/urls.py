"""Urls for the wishlist app."""
from django.urls import path
from .views import (
    WishlistDisplayView,
    AddRemoveProductWishlistAJAXView,
    EmptyWishlistAJAXView
)


urlpatterns = [
    path(
        'wishlist_display/',
        WishlistDisplayView.as_view(),
        name='wishlist_display'
    ),
    path(
        'add_remove_product_wishlist_ajax/',
        AddRemoveProductWishlistAJAXView.as_view(),
        name='add_remove_product_wishlist_ajax'
    ),
    path(
        'empty_wishlist_ajax/',
        EmptyWishlistAJAXView.as_view(),
        name='empty_wishlist_ajax'
    ),
]
