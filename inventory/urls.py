"""Urls for the inventory app."""
from django.urls import path
from .views import (
    ProductsListView,
    ProductDetailView,
)


urlpatterns = [
    path('store/', ProductsListView.as_view(), name='products_list'),
    path(
        'store/<int:pk>',
        ProductDetailView.as_view(),
        name='product_detail'
    ),
]
