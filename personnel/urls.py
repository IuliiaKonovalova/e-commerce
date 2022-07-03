"""Urls for the personnel app."""
from django.urls import path
from .views import (
    ProductsTableView,
    ProductFullDetailView,
    AddProductView,
)


urlpatterns = [
    path(
        'products_table/',
        ProductsTableView.as_view(),
        name='products_table'
    ),
    path(
        'product/<int:pk>/',
        ProductFullDetailView.as_view(),
        name='product_detail_full'
    ),
    path(
        'product/add/',
        AddProductView.as_view(),
        name='add_product'
    ),
]
