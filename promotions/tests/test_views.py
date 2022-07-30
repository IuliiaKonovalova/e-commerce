"""Tests for promotions views."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import Role, Profile
from promotions.models import Promotion
from datetime import datetime
from django.utils import timezone


class PromotionsListViewTest(TestCase):
    """Tests for the promotions list view."""

    def setUp(self):
        """Set up the test."""
        # create users
        self.role1 = Role.objects.create(
            name='Customer',
            description='Customer'
        )
        self.role2 = Role.objects.create(
            name='Manager',
            description='Manager'
        )
        self.role3 = Role.objects.create(
            name='Admin',
            description='Admin'
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
        self.user3 = User.objects.create_user(
            username='testuser3',
            password='Password987',
            email='admin@gmail.com'
        )
        self.profile1 = Profile.objects.get(id=self.user.profile.id)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        # Create promotion
        self.promotion = Promotion.objects.create(
            name='Promotion 1',
            slug='promotion-1',
            description='Promotion 1 description',
            promotion_code='PROMO1',
            promotion_reduction=10,
            start_date=datetime.now(),
            end_date=datetime.now() + timezone.timedelta(days=365 * 5),
            active=True,
        )
        # urls
        self.client = Client()
        self.promotions_list_url = reverse('promotions_list')
        self.add_promotion_url = reverse('add_promotion')
        self.edit_promotion_url = reverse('edit_promotion', args=['1'])
        self.delete_promotion_url = reverse('delete_promotion')

    def test_promotions_list_view_status_code(self):
        """Test the status code for the promotions list view."""
        response = self.client.get(self.promotions_list_url)
        self.assertEquals(response.status_code, 200)

    def test_promotions_list_view_template_used(self):
        """Test the template used for the promotions list view."""
        response = self.client.get(self.promotions_list_url)
        self.assertTemplateUsed(response, 'account/login.html')
        # customers login
        self.client.force_login(self.user)
        response = self.client.get(self.promotions_list_url)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()
        # manager login
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.promotions_list_url)
        self.assertTemplateUsed(response, 'promotions/promotions_list.html')
        self.client.logout()

    def test_add_promotion_view_status_code(self):
        """Test the status code for the add promotion view."""
        response = self.client.get(self.add_promotion_url)
        self.assertEquals(response.status_code, 200)

    def test_add_promotion_view_template_used(self):
        """Test the template used for the add promotion view."""
        response = self.client.get(self.add_promotion_url)
        self.assertTemplateUsed(response, 'account/login.html')
        # customers login
        self.client.force_login(self.user)
        response = self.client.get(self.add_promotion_url)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()
        # manager login
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(self.add_promotion_url)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()
        # admin login
        self.client.force_login(self.user3)
        self.assertTrue(self.profile3.role.id == 3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(self.add_promotion_url)
        self.assertTemplateUsed(response, 'promotions/add_promotion.html')
        self.client.logout()

    def test_add_promotion_view_post_request_logged_out(self):
        """Test the post request for the add promotion view."""
        response = self.client.post(self.add_promotion_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_add_promotion_view_post_request_not_staff(self):
        """Test the post request for the add promotion view."""
        # customers login
        self.client.force_login(self.user)
        response = self.client.post(self.add_promotion_url)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_promotion_view_post_request_staff_form_valid(self):
        # manager login
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(self.add_promotion_url, {
            'name': 'Promotion 2',
            'slug': 'promotion-2',
            'description': 'Promotion 2 description',
            'promotion_code': 'PROMO2',
            'promotion_reduction': 10,
            'start_date': datetime.now(),
            'end_date': datetime.now() + timezone.timedelta(days=365 * 5),
            'active': True,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_add_promotion_view_post_request_admin_form_valid(self):
        # admin login
        self.client.force_login(self.user3)
        self.assertTrue(self.profile3.role.id == 3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.post(self.add_promotion_url, {
            'name': 'Promotion 2',
            'slug': 'promotion-2',
            'description': 'Promotion 2 description',
            'promotion_code': 'PROMO2',
            'promotion_reduction': 10,
            'start_date': datetime.now(),
            'end_date': datetime.now() + timezone.timedelta(days=365 * 5),
            'active': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/promotions/promotions_list/')
        self.client.logout()

    def test_add_promotion_view_post_request_admin_form_not_valid(self):
        # admin login
        self.client.force_login(self.user3)
        self.assertTrue(self.profile3.role.id == 3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.post(self.add_promotion_url, {
            'slug': 'promotion-2',
            'description': 'Promotion 2 description',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'promotions/add_promotion.html')
        self.client.logout()

    def test_edit_promotion_view_status_code(self):
        """Test the status code for the edit promotion view."""
        response = self.client.get(
            reverse('edit_promotion', args=[self.promotion.id])
        )
        self.assertEquals(response.status_code, 200)

    def test_edit_promotion_view_template_used_logged_out(self):
        """Test the template used for the edit promotion view."""
        response = self.client.get(
            reverse(
                'edit_promotion',
                args=[self.promotion.id]
            )
        )
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_promotion_view_template_used_not_staff(self):
        # customers login
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('edit_promotion', args=[self.promotion.id])
        )
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_promotion_view_template_used_staff(self):
        # manager login
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.get(
            reverse('edit_promotion', args=[self.promotion.id])
        )
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_promotion_view_template_used_admin(self):
        # admin login
        self.client.force_login(self.user3)
        self.assertTrue(self.profile3.role.id == 3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.get(
            reverse('edit_promotion', args=[self.promotion.id])
        )
        self.assertTemplateUsed(response, 'promotions/edit_promotion.html')
        # check that the context has form
        self.assertIn('form', response.context)
        self.client.logout()

    def test_edit_promotion_view_post_request_logged_out(self):
        """Test the post request for the edit promotion view."""
        response = self.client.post(
            reverse('edit_promotion', args=[self.promotion.id])
        )
        self.assertTemplateUsed(response, 'account/login.html')

    def test_edit_promotion_view_post_request_not_staff(self):
        """Test the post request for the edit promotion view."""
        # customers login
        self.client.force_login(self.user)
        response = self.client.post(reverse(
            'edit_promotion',
            args=[self.promotion.id])
        )
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_promotion_view_post_request_staff_form_valid(self):
        # manager login
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            reverse('edit_promotion', args=[self.promotion.id]),
            {
                'name': 'Promotion 2',
                'slug': 'promotion-2',
                'description': 'Promotion 2 description',
                'promotion_code': 'PROMO2',
                'promotion_reduction': 10,
                'start_date': datetime.now(),
                'end_date': datetime.now() + timezone.timedelta(days=365 * 5),
                'active': True,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_edit_promotion_view_post_request_admin_form_valid(self):
        # admin login
        self.client.force_login(self.user3)
        self.assertTrue(self.profile3.role.id == 3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.post(
            reverse('edit_promotion', args=[self.promotion.id]),
            {
                'name': 'Promotion 2',
                'slug': 'promotion-2',
                'description': 'Promotion 2 description',
                'promotion_code': 'PROMO2',
                'promotion_reduction': 10,
                'start_date': datetime.now(),
                'end_date': datetime.now() + timezone.timedelta(days=365 * 5),
                'active': True,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/promotions/promotions_list/')
        self.client.logout()

    def test_edit_promotion_view_post_request_admin_form_not_valid(self):
        # admin login
        self.client.force_login(self.user3)
        self.assertTrue(self.profile3.role.id == 3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.post(
            reverse('edit_promotion', args=[self.promotion.id]),
            {
                'slug': 'promotion-2',
                'description': 'Promotion 2 description',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'promotions/edit_promotion.html')
        self.client.logout()

    def test_delete_promotion_ajax_view_post_request_logged_out(self):
        """Test the get request for the delete promotion view."""
        response = self.client.post(
            self.delete_promotion_url,
            {
                'promotion_id': 1,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertTemplateUsed(response, 'account/login.html')

    def test_delete_promotion_ajax_view_post_request_not_staff(self):
        """Test the get request for the delete promotion view."""
        # customers login
        self.client.force_login(self.user)
        response = self.client.post(
            self.delete_promotion_url,
            {
                'promotion_id': 1,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_promotion_ajax_view_post_request_staff(self):
        """Test the get request for the delete promotion view."""
        # manager login
        self.client.force_login(self.user2)
        self.assertFalse(self.profile2.role.id == 1)
        self.profile2 = Profile.objects.get(id=self.user2.profile.id)
        self.profile2.role = self.role2
        self.profile2.save()
        response = self.client.post(
            self.delete_promotion_url,
            {
                'promotion_id': 1,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/access_denied.html')
        self.client.logout()

    def test_delete_promotion_ajax_view_post_request_admin(self):
        """Test the get request for the delete promotion view."""
        # admin login
        self.client.force_login(self.user3)
        self.assertTrue(self.profile3.role.id == 3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.post(
            self.delete_promotion_url,
            {
                'promotion_id': 1,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.client.logout()

    def test_delete_promotion_ajax_view_post_request_admin_failed(self):
        """Test the get request for the delete promotion view."""
        # admin login
        self.client.force_login(self.user3)
        self.assertTrue(self.profile3.role.id == 3)
        self.profile3 = Profile.objects.get(id=self.user3.profile.id)
        self.profile3.role = self.role3
        self.profile3.save()
        response = self.client.post(
            self.delete_promotion_url,
            {
                'promotion_id': 1,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.client.logout()
