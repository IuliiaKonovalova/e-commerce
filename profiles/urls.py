"""Urls for the profile app."""
from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('<str:user>/', UserProfileView.as_view(), name='my_profile'),
]