"""Tests reviews urls."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reviews.views import (
    AddReviewView,
)


class TestUrls(SimpleTestCase):
    """Test reviews urls"""
    def test_add_review_url(self):
        """Test add review url"""
        url = reverse(
            'add_review',
            kwargs={'order_id': 1, 'product': 1}
        )
        self.assertEquals(resolve(url).func.view_class, AddReviewView)
