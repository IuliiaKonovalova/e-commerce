"""Tests reviews urls."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reviews.views import (
    ReviewDetailView,
    AddReviewView,
    AddReviewWithImagesAJAXView,
    ViewUsersReviewsView,
    ViewAllProductsReviewsView,
)


class TestUrls(SimpleTestCase):
    """Test reviews urls"""
    def test_review_url(self):
        """Test review url"""
        url = reverse(
            'review',
            kwargs={'order_id': 1, 'product_id': 1}
        )
        self.assertEquals(resolve(url).func.view_class, ReviewDetailView)

    def test_add_review_url(self):
        """Test add review url"""
        url = reverse(
            'add_review',
            kwargs={'order_id': 1, 'product_id': 1}
        )
        self.assertEquals(resolve(url).func.view_class, AddReviewView)

    def test_add_review_with_images_ajax_url(self):
        """Test add review with images AJAX url"""
        url = reverse('add_review_with_images_ajax')
        self.assertEquals(
            resolve(url).func.view_class, AddReviewWithImagesAJAXView
        )

    def test_view_users_reviews_url(self):
        """Test view users reviews url"""
        url = reverse('view_users_reviews')
        self.assertEquals(
            resolve(url).func.view_class, ViewUsersReviewsView
        )

    def test_view_all_products_reviews_url(self):
        """Test view all products reviews url"""
        url = reverse('view_all_products_reviews', kwargs={'product_id': 1})
        self.assertEquals(
            resolve(url).func.view_class, ViewAllProductsReviewsView
        )
