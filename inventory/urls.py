"""Urls for the inventory app."""
from django.urls import path
from .views import (
    ProductsListView,

)

urlpatterns = [
    path('store', ProductsListView.as_view(), name='products_list'),

]