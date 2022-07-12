"""Urls for payment app."""
from django.urls import path
from .views import (
    BasketView,

)


urlpatterns = [
    path('', BasketView, name='payment'),

]
