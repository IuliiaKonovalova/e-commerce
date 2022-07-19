"""Urls for Orders app."""
from django.urls import path
from .views import (
    OrdersView,
    OrderDetailsView,
    UpdateOrderStatusAJAXView,
    AddOrderAJAXView,
    EditOrderView,
    DeleteOrderView,
    EditOrderItemView,
    DeleteOrderItemView,
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
        'edit/<int:order_id>/',
        EditOrderView.as_view(),
        name='edit'
    ),
    path(
        'delete/<int:order_id>/',
        DeleteOrderView.as_view(),
        name='delete'
    ),
    path(
        'edit_order_item/<int:order_item_id>/',
        EditOrderItemView.as_view(),
        name='edit_order_item'
    ),
    path(
        'delete_order_item/<int:order_item_id>/',
        DeleteOrderItemView.as_view(),
        name='delete_order_item'
    ),
    path(
        '<str:user>/my_orders/',
        UserOrdersView.as_view(),
        name='my_orders'
    ),
    path(
        '<str:user>/my_orders/<str:order_number>/',
        UserOrderDetailsView.as_view(),
        name='my_order_details'
    ),
]
