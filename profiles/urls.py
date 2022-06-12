"""Urls for the profile app."""
from django.urls import path
from .views import (
    UserProfileView,
    EditAvatarAjaxView,
    ResetAvatarView,
    EditUserProfileView,
    DeleteProfileView,
    AddressesView,
    AddAddressView,
    EditAddressView,
    DeleteAddressView,
    ChangePrimaryAddressView,
)

urlpatterns = [
    path(
        'my_profile/edit_avatar/',
        EditAvatarAjaxView.as_view(),
        name='edit_avatar_ajax'
    ),
    path(
        'my_profile/reset_avatar/',
        ResetAvatarView.as_view(),
        name='reset-avatar'
    ),
    path(
        'my_profile/delete/',
        DeleteProfileView.as_view(),
        name='delete-user'
    ),
    path(
        '<str:user>/',
        UserProfileView.as_view(),
        name='my_profile'
    ),
    path(
        '<str:user>/edit/',
        EditUserProfileView.as_view(),
        name='edit_profile'
    ),
    path(
        '<str:user>/addresses/',
        AddressesView.as_view(),
        name='my_addresses'
    ),
    path(
        '<str:user>/addresses/add/',
        AddAddressView.as_view(),
        name='add_address'
    ),
    path(
        '<str:user>/addresses/<int:pk>/edit/',
        EditAddressView.as_view(),
        name='edit_address'
    ),
    path(
        '<str:user>/addresses/<int:pk>/delete/',
        DeleteAddressView.as_view(),
        name='delete_address'
    ),
    path(
        'my_addresses/set_primary',
        ChangePrimaryAddressView.as_view(),
        name='set_primary_address'
    ),
]
