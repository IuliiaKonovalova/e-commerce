"""Tests for the models of the profiles app."""
from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Role, Profile, Address
import cloudinary
import cloudinary.uploader
from datetime import date


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
        self.address1 = Address.objects.create(
            user=self.user,
            country='USA',
            county_region='California',
            city='San Francisco',
            address_line='123 Main St',
            zip_code='12345',
            phone_number='1234567890',
            is_primary=False,
            created_at='2020-01-01',
            updated_at='2020-01-01'
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
        self.assertEqual(
            Profile.objects.get(user=self.user2).user,
            self.user2
        )

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
        profile.first_name = 'Test2First'
        profile.last_name = 'Test2Last'
        profile.birthday = '2000-01-01'
        profile.subscription = True
        self.assertEqual(profile.first_name, 'Test2First')
        self.assertEqual(profile.last_name, 'Test2Last')
        self.assertEqual(profile.birthday, '2000-01-01')
        self.assertEqual(profile.subscription, True)

    def test_profile_str(self):
        """Test profile string representation."""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), 'testuser')
        profile.first_name = 'Test2First'
        self.assertEqual(str(profile), 'Test2First')
        profile.last_name = 'Test2Last'
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

    def test_profile_age(self):
        """Test profile age property."""
        profile = Profile.objects.get(user=self.user2)
        self.assertEqual(profile.age, None)
        profile.birthday = date(1990, 1, 1)
        self.assertEqual(profile.age, 32)
        profile.birthday = date(4990, 1, 1)
        self.assertEqual(profile.age, 'Invalid birthday')
        profile.birthday = date(1999, 1, 1)
        self.assertEqual(profile.age, 23)
        profile.birthday = date(2000, 1, 1)
        self.assertEqual(profile.age, 22)

    def test_address_creation(self):
        """Test address creation."""
        self.assertEqual(Address.objects.all().count(), 1)

    def test_address_user(self):
        """Test the user field."""
        address = Address.objects.get(id=1)
        self.assertEqual(address.user.username, 'testuser')
        self.assertEqual(address.country, 'USA')
        self.assertEqual(address.county_region, 'California')
        self.assertEqual(address.city, 'San Francisco')
        self.assertEqual(address.address_line, '123 Main St')
        self.assertEqual(address.zip_code, '12345')
        self.assertEqual(address.phone_number, '1234567890')
        self.assertEqual(address.is_primary, False)

    def test_address_str(self):
        """Test address string representation."""
        address = Address.objects.get(id=1)
        self.assertEqual(str(address), 'testuser - 12345 - False')

    def test_address_is_primary(self):
        """Test address is_primary property."""
        self.address2 = Address.objects.create(
            user=self.user,
            country='Canada',
            county_region='Ontario',
            city='Toronto',
            address_line='456 Main St',
            zip_code='54321',
            phone_number='0987654321',
            is_primary=True,
            created_at='2020-01-01',
            updated_at='2020-01-01'
        )
        self.assertEqual(self.address2.is_primary, True)
        self.address3 = Address.objects.create(
            user=self.user,
            country='USA',
            county_region='California',
            city='San Francisco',
            address_line='999 Main St',
            zip_code='13000',
            phone_number='1234567890',
            is_primary=True,
            created_at='2020-01-01',
            updated_at='2020-01-01'
        )
        # Check whether the primary address is updated for address2
        address2 = Address.objects.get(id=2)
        self.assertEqual(address2.is_primary, False)
        self.assertEqual(self.address3.is_primary, True)
