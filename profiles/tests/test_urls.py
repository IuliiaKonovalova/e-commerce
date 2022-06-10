"""Test Profiles URLs."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from profiles.views import (
    UserProfileView,
    EditAvatarAjaxView,
    ResetAvatarView,
    EditUserProfileView
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