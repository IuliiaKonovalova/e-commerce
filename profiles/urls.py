"""Urls for the profile app."""
from django.urls import path
from .views import (
    UserProfileView,
    EditAvatarAjaxView,
    ResetAvatarView,
    EditUserProfileView,
    DeleteProfileView
)

urlpatterns = [
    path('my_profile/edit_avatar/', EditAvatarAjaxView.as_view(), name='edit_avatar_ajax'),
    path('my_profile/reset_avatar/', ResetAvatarView.as_view(), name='reset-avatar'),
    path('my_profile/delete/', DeleteProfileView.as_view(), name='delete-user'),
    path('<str:user>/', UserProfileView.as_view(), name='my_profile'),
    path('<str:user>/edit/', EditUserProfileView.as_view(), name='edit_profile'),
]