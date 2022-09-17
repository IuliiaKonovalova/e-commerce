"""Tests for the views of the profile app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import Role, Profile, Address
from django.contrib.auth.hashers import make_password


class TestViews(TestCase):
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
        self.client = Client()
        self.user_profile_url = reverse(
            'my_profile',
            kwargs={'user': 'testuser'}
        )
        self.edit_user_profile_url = reverse(
            'edit_profile',
            kwargs={'user': 'testuser'}
        )
        self.edit_avatar_url = reverse('edit_avatar_ajax')
        self.reset_avatar_url = reverse('reset-avatar')
        self.delete_user_url = reverse('delete_profile')
        self.addresses_url = reverse(
            'my_addresses',
            kwargs={'user': 'testuser'}
        )
        self.add_address_url = reverse(
            'add_address',
            kwargs={'user': 'testuser'}
        )
        self.edit_address_url = reverse(
            'edit_address',
            kwargs={'user': 'testuser', 'pk': 1}
        )
        self.delete_address_url = reverse(
            'delete_address',
            kwargs={'user': 'testuser', 'pk': 1}
        )
        self.change_primary_ajax_url = reverse(
            'set_primary_address',
        )

    def test_user_profile_view(self):
        """Test user profile view."""
        self.client.force_login(self.user)
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/my_profile.html')
        self.client.logout()
        response = self.client.get(self.user_profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_avatar_ajax_view(self):
        """Test edit avatar ajax view."""
        self.client.force_login(self.user)
        avatar = open('static/images/default_testing_avatar.jpg', 'rb')
        response = self.client.post(
            self.edit_avatar_url,
            {'avatar': avatar},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        # check whether AJAX response has failed
        self.client.logout()
        self.client.force_login(self.user)
        response = self.client.post(
            self.edit_avatar_url,
            {'avatar': avatar}
        )
        self.assertEqual(response.json()['success'], False)

    def test_reset_avatar_ajax_view(self):
        """Test reset avatar ajax view."""
        self.client.force_login(self.user)
        response = self.client.post(
            self.reset_avatar_url,
            {},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        # check whether AJAX response has failed
        self.client.logout()
        self.client.force_login(self.user)
        response = self.client.post(
            self.reset_avatar_url,
            {'avatar': 'test'}
        )
        self.assertEqual(response.json()['success'], False)

    def test_edit_profile_get_view(self):
        """Test edit profile get view."""
        self.client.force_login(self.user)
        response = self.client.get(self.edit_user_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/edit_profile.html')
        self.assertIn('profile_form', response.context)
        self.assertIn('password_form', response.context)
        self.client.logout()
        response = self.client.get(self.edit_user_profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_profile_post_view(self):
        """Test edit profile post view."""
        self.client.force_login(self.user)
        response = self.client.post(
            self.edit_user_profile_url,
            data={
                'form_type': 'profile',
                'first_name': 'Test',
                'last_name': 'User',
                'birthday': '2020-01-01',
                'subscription': True
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        response = self.client.post(
            self.edit_user_profile_url,
            data={
                'form_type': 'profile',
                'first_name': 'Test',
                'last_name': 'User',
                'birthday': '20-01-01',
                'subscription': True
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.json()['success'], False)
        self.client.logout()
        pwd = make_password('123')
        self.user33 = User.objects.create(
            username='testuser33',
            password=pwd,
            email='user3gmail.com'
        )
        self.client.force_login(self.user33)
        pwd2 = make_password('12345')
        response = self.client.post(
            self.edit_user_profile_url,
            data={
                'form_type': 'password',
                'old_password': pwd,
                'new_password': pwd2,
                'confirm_password': pwd2
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        response = self.client.post(
            self.edit_user_profile_url,
            data={
                'form_type': 'password',
                'old_password': 'Password987',
                'new_password': 'Password987',
                'confirm_password': 'Password987'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.json()['success'], False)
        self.client.logout()
        response = self.client.post(
            self.edit_user_profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_profile_view(self):
        """Test delete profile view."""
        pwd = make_password('123')
        self.user33 = User.objects.create(
            username='testuser33',
            password=pwd,
            email='user3gmail.com'
        )
        self.client.force_login(self.user33)
        self.assertEqual(
            User.objects.filter(username='testuser33').count(),
            1
        )
        response = self.client.post(
            self.delete_user_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(
            User.objects.filter(username='testuser33').count(),
            1
        )
        response = self.client.post(
            self.delete_user_url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            User.objects.filter(username='testuser33').count(),
            0
        )
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

    def test_addresses_get_view(self):
        """Test addresses get view."""
        self.client.force_login(self.user)
        response = self.client.get(self.addresses_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/my_addresses.html')
        self.client.logout()
        response = self.client.get(self.addresses_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_address_get_view(self):
        """Test add address get view."""
        self.client.force_login(self.user)
        response = self.client.get(self.add_address_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/add_address.html')
        self.client.logout()
        response = self.client.get(self.add_address_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_address_post_view(self):
        """Test add address post view."""
        self.client.force_login(self.user)
        self.assertEqual(Address.objects.filter(user=self.user).count(), 1)
        response = self.client.post(
            self.add_address_url,
            data={
                'country': 'Test country',
                'county_region': 'Test county region',
                'city': 'Test city',
                'address_line': 'Test street',
                'zip_code': '99999',
                'phone_number': '123456789',
                'is_primary': True
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Address.objects.filter(user=self.user).count(), 2)
        self.assertEqual(response.url, self.addresses_url)
        response = self.client.post(
            self.add_address_url,
            data={
                'country': 'Test country',
                'county_region': 'Test county region',
                'city': 'Test city',
                'address_line': 'Test street',
                'zip_code': '12345',
                'phone_number': '',
                'is_primary': True
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/add_address.html')
        self.assertEqual(Address.objects.filter(user=self.user).count(), 2)
        self.client.logout()
        response = self.client.post(
            self.add_address_url,
            data={
                'country': 'Test country',
                'county_region': 'Test county region',
                'city': 'Test city',
                'address_line': 'Test street',
                'zip_code': '12345',
                'phone_number': '123456789',
                'is_primary': True
            },
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_address_get_view(self):
        """Test edit address get view."""
        self.client.force_login(self.user)
        response = self.client.get(self.edit_address_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/edit_address.html')
        self.client.logout()
        response = self.client.get(self.edit_address_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_address_post_view(self):
        """Test edit address post view."""
        self.client.force_login(self.user)
        response = self.client.post(
            self.edit_address_url,
            data={
                'country': 'Test country',
                'county_region': 'Test county region',
                'city': 'Test city',
                'address_line': 'Test street',
                'zip_code': '99999',
                'phone_number': '123456789',
                'is_primary': True
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.addresses_url)
        response = self.client.post(
            self.edit_address_url,
            data={
                'country': 'Test country',
                'county_region': 'Test county region',
                'city': 'Test city',
                'address_line': 'Test street',
                'zip_code': '12345',
                'phone_number': '',
                'is_primary': True
            },
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.post(
            self.edit_address_url,
            data={
                'country': 'Test country',
                'county_region': 'Test county region',
                'city': 'Test city',
                'address_line': 'Test street',
                'zip_code': '12345',
                'phone_number': '',
                'is_primary': True
            },
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_address_get_view(self):
        """Test delete address post view."""
        self.client.force_login(self.user)
        self.assertEqual(Address.objects.filter(user=self.user).count(), 1)
        response = self.client.get(self.delete_address_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Address.objects.filter(user=self.user).count(), 0)
        self.client.logout()
        response = self.client.get(self.delete_address_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_change_primary_ajax_view(self):
        """Test change primary ajax view."""
        self.client.force_login(self.user)
        user1 = self.user
        address1 = self.address1
        self.assertEqual(Address.objects.filter(user=user1).count(), 1)
        self.assertEqual(address1.is_primary, False)
        response = self.client.post(
            self.change_primary_ajax_url,
            {'address_id': address1.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.json()['success'], True)
        primary = Address.objects.get(id=address1.id).is_primary
        self.assertEqual(response.status_code, 200)
        self.assertEqual(primary, True)
        # Check that if address is primary, it will change to false
        address2 = Address.objects.create(
            user=self.user,
            country='USA',
            county_region='California',
            city='San Francisco',
            address_line='123 Main St',
            zip_code='9999',
            phone_number='1234567890',
            is_primary=True,
            created_at='2020-01-01',
            updated_at='2020-01-01'
        )
        self.assertEqual(Address.objects.filter(user=user1).count(), 2)
        self.assertEqual(address2.is_primary, True)
        response = self.client.post(
            self.change_primary_ajax_url,
            {'address_id': address2.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.json()['success'], True)
        primary = Address.objects.get(id=address2.id).is_primary
        self.assertEqual(response.status_code, 200)
        self.assertEqual(primary, False)
        # Check if the request is not ajax
        response = self.client.post(
            self.change_primary_ajax_url,
            {'address_id': address2.id}
        )
        self.assertEqual(response.json()['success'], False)
        self.client.logout()
