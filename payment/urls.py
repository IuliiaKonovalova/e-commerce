"""Urls for payment app."""
from django.urls import path
from .views import (
    BasketView,
    order_placed,

)


urlpatterns = [
    path('', BasketView, name='payment'),
    path('order_placed/', order_placed, name='order_placed'),

]
