"""Test for Home Views"""
from pydoc import resolve
from django.test import TestCase, Client
from django.urls import reverse


class TestHomeView(TestCase):
    """Test for Home Views"""

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')

    def test_home_status_code(self):
        """Test for Home Views"""
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)

    def test_home_template(self):
        """Test for Home Views"""
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'home/home.html')
