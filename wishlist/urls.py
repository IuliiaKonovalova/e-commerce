"""Urls for the wishlist app."""
from django.urls import path
from .views import (
    WishlistDisplayView,
)


urlpatterns = [
    path(
        'wishlist_display/',
        WishlistDisplayView.as_view(),
        name='wishlist_display'
    ),
]
