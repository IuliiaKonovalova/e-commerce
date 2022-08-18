"""Forms for the promotions app."""
from django import forms
from .models import Promotion


class PromotionForm(forms.ModelForm):
    """Form for the Promotion model."""
    class Meta:
        model = Promotion
        fields = [
            'name',
            'description',
            'promotion_code',
            'promotion_reduction',
            'start_date',
            'end_date',
            'products_inventory_in_promotion',
            'active',
        ]
        promotion_reduction = forms.DecimalField()
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Name',
                    'title': 'Promotion Name',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Description',
                    'title': 'Promotion Description',
                }
            ),
            'promotion_code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Promotion Code',
                    'title': 'Promotion Code',
                }
            ),
            'active': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                    'title': 'Promotion Active',
                }
            ),
            'start_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Start Date',
                    'title': 'Promotion Start Date',
                }
            ),
            'end_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'End Date',
                    'title': 'Promotion End Date',
                }
            ),
            'products_inventory_in_promotion': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'title': 'Select products inventory in promotion',
                    'multiple': 'multiple',
                }
            ),
        }
