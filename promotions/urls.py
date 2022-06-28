"""URLs for the promotion app."""
from django.urls import path
from .views import (
    PromotionsListView,
    AddPromotionView,
    EditPromotionView,
)


urlpatterns = [
    path(
        'promotions_list/',
        PromotionsListView.as_view(),
        name='promotions_list'
    ),
    path(
        'add_promotion/',
        AddPromotionView.as_view(),
        name='add_promotion'
    ),
    path(
        'edit_promotion/<int:pk>/',
        EditPromotionView.as_view(),
        name='edit_promotion'
    ),
]