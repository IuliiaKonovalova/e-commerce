"""Urls for the personnel app."""
from django.urls import path
from .views import (
    ProductsTableView,
)


urlpatterns = [
    path(
        'products_table/',
        ProductsTableView.as_view(),
        name='products_table'
    ),
]
