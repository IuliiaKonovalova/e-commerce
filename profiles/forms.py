"""Forms for the profiles app."""
from django import forms
from .models import Profile, Address


class ProfileForm(forms.ModelForm):
    """Form for the Profile model."""
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birthday', 'avatar', 'subscription']
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'First name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Last name',
                }
            ),
            'birthday': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'title': 'YYYY-MM-DD',
                    'placeholder': 'Birthday',
                }
            ),
            'avatar': forms.HiddenInput(),
            'subscription': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
        }

class AddressForm(forms.ModelForm):
    """Form for the Address model."""
    class Meta:
        model = Address
        fields = [
            'country',
            'county_region',
            'city',
            'address_line',
            'zip_code',
            'phone_number',
            'is_primary'
        ]
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
            'county_region': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'address_line': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

