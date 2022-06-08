"""Tests for the models of the profiles app."""
from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Role, Profile
import cloudinary
import cloudinary.uploader


class TestModels(TestCase):
    """Tests for the Roles model."""

    def setUp(self):
        """Set up the test."""
        self.role1 = Role.objects.create(
            name='Customer',
            description='Customer'
        )
        self.role2 = Role.objects.create(
            name='Manager',
            description='Manager'
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='Password987',
            email='testuser@gmail.com'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='Password987',
            email='testuser2@gmail.com'
        )

    def test_role_name(self):
        """Test the name field."""
        self.assertEqual(self.role1.name, 'Customer')
        self.assertEqual(self.role1.description, 'Customer')

    def test_role_str(self):
        """Test role string representation."""
        self.assertEqual(str(self.role1), 'Customer')
        self.assertEqual(str(self.role2), 'Manager')

    def test_profile_creation(self):
        """Test profile creation."""
        # profile should already exist because of signals
        self.assertEqual(Profile.objects.count(), 2)
        self.assertEqual(Profile.objects.get(user=self.user).user, self.user)
        self.assertEqual(Profile.objects.get(user=self.user2).user, self.user2)

    def test_profile_user(self):
        """Test the user field."""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.first_name, None)
        self.assertEqual(profile.last_name, None)
        self.assertEqual(profile.birthday, None)
        self.assertEqual(
            profile.avatar, None
        )
        self.assertEqual(profile.subscription, False)

    def test_profile_update(self):
        """Test the update method."""
        profile = Profile.objects.get(user=self.user)
        # profile.avatar=cloudinary.uploader.upload_image(
        #     "static/images/default_avatar.svg"
        # )
        profile.first_name='Test2First'
        profile.last_name='Test2Last'
        profile.birthday='2000-01-01'
        profile.subscription=True
        # self.assertTrue('res.cloudinary.com' in profile.avatar.url)
        self.assertEqual(profile.first_name, 'Test2First')
        self.assertEqual(profile.last_name, 'Test2Last')
        self.assertEqual(profile.birthday, '2000-01-01')
        self.assertEqual(profile.subscription, True)

    def test_profile_str(self):
        """Test profile string representation."""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), 'testuser')
        profile.first_name='Test2First'
        self.assertEqual(str(profile), 'Test2First')
        profile.last_name='Test2Last'
        self.assertEqual(str(profile), 'Test2First Test2Last')

    def test_profile_avatar_url(self):
        """Test profile avatar_url property."""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(
            profile.avatar_url,
            "/static/images/default_avatar.svg"
        )
        profile.avatar = cloudinary.uploader.upload_image(
            "static/images/default_avatar.svg")
        profile.save()
        self.assertTrue('res.cloudinary.com' in profile.avatar_url)