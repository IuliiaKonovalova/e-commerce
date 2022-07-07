"""Urls for the personnel app."""
from django.urls import path
from .views import (
    ProductsTableView,
    ProductFullDetailView,
    AddProductView,
    EditProductView,
    DeleteProductView,
    AddImageToProductAJAXView,
    EditImageToProductAJAXView,
    DeleteImageToProductAJAXView,
    ProductInventoryDetailsView,
    AddProductInventoryDetailsView,
    GetTypeAttributeAJAXView,
    ProductInventoryCreateAJAXView,
    EditProductInventoryView,
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
    path(
        'product/<int:pk>/edit/',
        EditProductView.as_view(),
        name='edit_product'
    ),
    path(
        'product/<int:pk>/delete/',
        DeleteProductView.as_view(),
        name='delete_product'
    ),
    path(
        'add_product_image/',
        AddImageToProductAJAXView.as_view(),
        name='add_product_image'
    ),
    path(
        'edit_product_image/',
        EditImageToProductAJAXView.as_view(),
        name='edit_product_image'
    ),
    path(
        'delete_product_image/',
        DeleteImageToProductAJAXView.as_view(),
        name='delete_product_image'
    ),
    path(
        'product/<int:pk>/inventory/<int:inventory_pk>/',
        ProductInventoryDetailsView.as_view(),
        name='product_inventory_details'
    ),
    path(
        'product/<int:pk>/add_inventory/',
        AddProductInventoryDetailsView.as_view(),
        name='add_product_inventory_details'
    ),
    path(
        'get_type_attribute/',
        GetTypeAttributeAJAXView.as_view(),
        name='get_type_attribute'
    ),
    path(
        'product_inventory_create',
        ProductInventoryCreateAJAXView.as_view(),
        name='product_inventory_create'
    ),
    path(
        'product/<int:pk>/edit_inventory/<int:inventory_pk>/',
        EditProductInventoryView.as_view(),
        name='edit_product_inventory'
    ),
]
