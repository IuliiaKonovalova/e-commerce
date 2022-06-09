"""Forms for the profiles app."""
from django import forms
from .models import Profile, Address


class ProfileForm(forms.ModelForm):
    """Form for the Profile model."""
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birthday', 'avatar', 'subscription']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={
                    'multiple': False,
                    'class': 'edit-avatar-btn'
                }),
            'subscription': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
        }