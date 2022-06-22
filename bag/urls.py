"""Urls for the bag app."""
from django.urls import path
from .views import (
    BagDisplayView,
)


urlpatterns = [
    path('bag_display/', BagDisplayView.as_view(), name='bag_display'),
]
