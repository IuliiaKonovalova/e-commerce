"""Urls for Orders app."""
from django.urls import path
from .views import (
    OrdersView,
    OrderDetailsView,
    UpdateOrderStatusAJAXView,
    AddOrderAJAXView,
    UserOrdersView,
    UserOrderDetailsView,
)


urlpatterns = [
    path('', OrdersView.as_view(), name='orders'),
    path(
        'order_details/<int:order_id>/',
        OrderDetailsView.as_view(),
        name='order_details'
    ),
    path(
        'update_order_status/',
        UpdateOrderStatusAJAXView.as_view(),
        name='update_order_status'
    ),
    path(
        'add/',
        AddOrderAJAXView.as_view(),
        name='add'
    ),
    path(
        '<str:user>/my_orders/',
        UserOrdersView.as_view(),
        name='my_orders'
    ),
    path(
        '<str:user>/my_orders/<int:order_id>/',
        UserOrderDetailsView.as_view(),
        name='my_order_details'
    ),
]
