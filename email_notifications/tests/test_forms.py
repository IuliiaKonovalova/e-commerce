"""Test for email notification form"""
from django.test import TestCase
from email_notifications.forms import EmailNewsNotificationForm


class EmailNewsNotificationFormTest(TestCase):
    """Test for email notification form"""
    def test_email_news_notification_form_has_fields(self):
        """Test for email news notification form has fields"""
        form = EmailNewsNotificationForm()
        self.assertEqual(len(form.fields), 3)

    def test_email_news_notification_form_is_valid(self):
        """Test for email news notification form is valid"""
        form = EmailNewsNotificationForm({
            'email_name': 'Test',
            'content': 'Test',
        })
        self.assertTrue(form.is_valid())

    def test_email_news_notification_form_is_invalid(self):
        """Test for email news notification form is invalid"""
        form = EmailNewsNotificationForm({
            'email_name': '',
            'content': '',
        })
        self.assertFalse(form.is_valid())

    def test_email_news_notification_form_is_invalid_email_name(self):
        """Test for email news notification form is invalid email name"""
        form = EmailNewsNotificationForm({
            'email_name': '',
            'content': 'Test',
        })
        self.assertFalse(form.is_valid())

    def test_email_news_notification_form_is_invalid_content(self):
        """Test for email news notification form is invalid content"""
        form = EmailNewsNotificationForm({
            'email_name': 'Test',
            'content': '',
        })
        self.assertFalse(form.is_valid())
