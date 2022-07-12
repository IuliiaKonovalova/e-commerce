"""Urls for Orders app."""
from django.urls import path
from .views import (
    OrdersView,
)


urlpatterns = [
    path('', OrdersView.as_view(), name='orders'),

]
