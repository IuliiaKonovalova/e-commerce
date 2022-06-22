"""Urls for the bag app."""
from django.urls import path
from .views import (
    BagDisplayView,
    AddToBagAJAXView,
)


urlpatterns = [
    path('bag_display/', BagDisplayView.as_view(), name='bag_display'),
    path(
        'add_to_bag/',
        AddToBagAJAXView.as_view(),
        name='add_to_bag'
    ),
]
