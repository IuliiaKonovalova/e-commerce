"""Tests for promotions urls."""
from django.test import TestCase
from django.urls import reverse

from promotions.views import (
    PromotionsListView,
)


class PromotionsListViewTest(TestCase):
    """Tests for the promotions list view."""
    def test_promotions_list_view_status_code(self):
        """Test the status code for the promotions list view."""
        url = reverse('promotions_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


