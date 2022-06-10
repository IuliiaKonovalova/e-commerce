"""Tests for the views of the profile app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import Role, Profile, Address
import cloudinary
import cloudinary.uploader
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
        self.delete_user_url = reverse('delete-user')

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
            password = pwd,
            email='user3gmail.com'
        )
        self.client.force_login(self.user33)
        pwd2 = make_password('12345')
        print('User password', self.user33.password)
        print(pwd)
        print(pwd2)
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
            password = pwd,
            email='user3gmail.com'
        )
        self.client.force_login(self.user33)
        self.assertEqual(User.objects.filter(username='testuser33').count(), 1)
        response = self.client.post(
            self.delete_user_url,
            data={
                'password': 'pwd'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.filter(username='testuser33').count(), 0)
        response = self.client.post(
            self.delete_user_url,
            data={
                'password': 'pwd'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

