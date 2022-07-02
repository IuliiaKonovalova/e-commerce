"""Urls for the personnel app."""
from django.urls import path
from .views import (
    ProductsTableView,
    ProductDetailView,
)


urlpatterns = [
    path(
        'products_table/',
        ProductsTableView.as_view(),
        name='products_table'
    ),
    path(
        'product/<int:pk>/',
        ProductDetailView.as_view(),
        name='product_detail'
    ),
    
]
