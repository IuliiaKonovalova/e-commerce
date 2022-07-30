"""Tests for promotions urls."""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from promotions.views import (
    PromotionsListView,
    AddPromotionView,
    EditPromotionView,
    DeletePromotionAJAXView,
)


class TestUrls(SimpleTestCase):
    """Tests for the promotions urls."""
    def test_promotions_list_url(self):
        """Test the promotions list url."""
        url = reverse('promotions_list')
        self.assertEquals(resolve(url).func.view_class, PromotionsListView)

    def test_add_promotion_url(self):
        """Test the add promotion url."""
        url = reverse('add_promotion')
        self.assertEquals(resolve(url).func.view_class, AddPromotionView)

    def test_edit_promotion_url(self):
        """Test the edit promotion url."""
        url = reverse('edit_promotion', kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, EditPromotionView)

    def test_delete_promotion_url(self):
        """Test the delete promotion url."""
        url = reverse('delete_promotion')
        self.assertEquals(
            resolve(url).func.view_class,
            DeletePromotionAJAXView
        )
