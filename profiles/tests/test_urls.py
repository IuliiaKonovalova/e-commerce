"""Test Profiles URLs."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from profiles.views import (
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


class TestUrls(SimpleTestCase):
    """Test Profiles URLs."""

    def test_profile_url(self):
        """Test profile url."""
        url = reverse('my_profile', kwargs={'user': 'testuser'})
        self.assertEquals(resolve(url).func.view_class, UserProfileView)

    def test_edit_avatar_url(self):
        """Test edit avatar url."""
        url = reverse('edit_avatar_ajax')
        self.assertEquals(resolve(url).func.view_class, EditAvatarAjaxView)

    def test_reset_avatar_url(self):
        """Test reset avatar url."""
        url = reverse('reset-avatar')
        self.assertEquals(resolve(url).func.view_class, ResetAvatarView)

    def test_edit_user_profile_url(self):
        """Test edit user profile url."""
        url = reverse('edit_profile', kwargs={'user': 'testuser'})
        self.assertEquals(resolve(url).func.view_class, EditUserProfileView)

    def test_delete_profile_url(self):
        """Test delete profile url."""
        url = reverse('delete_profile')
        self.assertEquals(resolve(url).func.view_class, DeleteProfileView)

    def test_addresses_url(self):
        """Test addresses url."""
        url = reverse('my_addresses', kwargs={'user': 'testuser'})
        self.assertEquals(resolve(url).func.view_class, AddressesView)

    def test_add_address_url(self):
        """Test add address url."""
        url = reverse('add_address', kwargs={'user': 'testuser'})
        self.assertEquals(resolve(url).func.view_class, AddAddressView)

    def test_edit_address_url(self):
        """Test edit address url."""
        url = reverse('edit_address', kwargs={'user': 'testuser', 'pk': 1})
        self.assertEquals(resolve(url).func.view_class, EditAddressView)

    def test_delete_address_url(self):
        """Test delete address url."""
        url = reverse('delete_address', kwargs={'user': 'testuser', 'pk': 1})
        self.assertEquals(resolve(url).func.view_class, DeleteAddressView)

    def test_change_primary_address_url(self):
        """Test change primary address url."""
        url = reverse('set_primary_address')
        self.assertEquals(
            resolve(url).func.view_class,
            ChangePrimaryAddressView
        )
