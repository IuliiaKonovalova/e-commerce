"""Urls for the bag app."""
from django.urls import path
from .views import (
    BagDisplayView,
    AddToBagAJAXView,
    RemoveUnitFromBagAJAXView,
    AddUnitToBagAJAXView,
)


urlpatterns = [
    path('bag_display/', BagDisplayView.as_view(), name='bag_display'),
    path(
        'add_to_bag/',
        AddToBagAJAXView.as_view(),
        name='add_to_bag'
    ),
    path(
        'remove_unit_from_bag/',
        RemoveUnitFromBagAJAXView.as_view(),
        name='remove_unit_from_bag'
    ),
    path(
        'add_unit_to_bag/',
        AddUnitToBagAJAXView.as_view(),
        name='add_unit_to_bag'
    ),

]
