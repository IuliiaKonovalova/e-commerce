"""Tests reviews urls."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reviews.views import (
    ReviewDetailView,
    AddReviewView,

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
            kwargs={'order_id': 1, 'product': 1}
        )
        self.assertEquals(resolve(url).func.view_class, AddReviewView)


