"""Urls for the inventory app."""
from django.urls import path
from .views import (
    ProductsListView,
    ProductDetailView,
    ProductAttributeAJAXView,
)

urlpatterns = [
    path('store', ProductsListView.as_view(), name='products_list'),
    path(
        'store/<int:pk>',
        ProductDetailView.as_view(),
        name='product_detail'
    ),
    path(
        'product_attribute_value_update',
        ProductAttributeAJAXView.as_view(),
        name='product_attribute_value_update'
    ),
]