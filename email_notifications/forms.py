"""Forms for email notifications."""
from django import forms
from .models import EmailNewsNotification


class EmailNewsNotificationForm(forms.ModelForm):
    """Form for email news notifications."""
    class Meta:
        """Meta class for email news notifications."""
        model = EmailNewsNotification
        fields = ['email_name', 'content', 'code']

        widgets = {
            'email_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add email name',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add email content',
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add code if the email is promotional',
            }),
        }
