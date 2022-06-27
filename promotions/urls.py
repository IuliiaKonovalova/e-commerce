"""URLs for the promotion app."""
from django.urls import path
from .views import (
    PromotionsListView
)


urlpatterns = [
    path(
        'promotions_list/',
        PromotionsListView.as_view(),
        name='promotions_list'
    ),
]