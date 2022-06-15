"""Forms for the inventory app."""
from django import forms
from .models import (
    Category,
    Tag,
    Brand,
    Product,
    ProductImage,
    ProductAttribute,
    ProductType,
    ProductAttributeValue,
    ProductInventory,
    Stock,
    ProductAttributeValues,
    ProductTypeAttribute,
)


class CategoryForm(forms.ModelForm):
    """Form for the Category model."""
    class Meta:
        model = Category
        fields = ['name', 'slug', 'is_active']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Category Name',
                }
            ),
            'slug': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Category Slug Name',
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
        }


class TagForm(forms.ModelForm):
    """Form for the Tag model."""
    class Meta:
        model = Tag
        fields = ['name', 'slug', 'is_active']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Tag Name',
                }
            ),
            'slug': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Tag Slug Name',
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
        }
