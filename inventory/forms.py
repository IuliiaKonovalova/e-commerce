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


class BrandForm(forms.ModelForm):
    """Form for the Brand model."""
    class Meta:
        model = Brand
        fields = ['name', 'slug', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Brand Name',
                }
            ),
            'slug': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Brand Slug Name',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=500',
                    'placeholder': 'Brand Description',
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
        }


class ProductForm(forms.ModelForm):
    """Form for the Product model."""
    class Meta:
        model = Product
        fields = [
            'name',
            'slug',
            'description',
            'category',
            'tags',
            'brand',
            'is_active'
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Product Type Name',
                }
            ),
            'slug': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Product Type Slug Name',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=500',
                    'placeholder': 'Product Type Description',
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-control',
                    'title': 'select a category',
                    'placeholder': 'Product Type Category',
                }
            ),
            'tags': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'title': 'select tags',
                    'placeholder': 'Product Type Tags',
                }
            ),
            'brand': forms.Select(
                attrs={
                    'class': 'form-control',
                    'title': 'select a brand',
                    'placeholder': 'Product Type Brand',
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
        }


class ProductImageForm(forms.ModelForm):
    """Form for the ProductImage model."""
    class Meta:
        model = ProductImage
        fields = ['product', 'image', 'alt_text', 'is_active']
        widgets = {
            'product': forms.Select(
                attrs={
                    'class': 'form-control',
                    'title': 'select a product',
                    'placeholder': 'Product Image Product',
                }
            ),
            'image': forms.ClearableFileInput(
                attrs={'multiple': False, 'accept': 'image/*'}
            ),
            'alt_text': forms.TextInput(
                attrs={
                  'rows': 3,
                  'class': 'form-control',
                  'title': 'max_length=50',
                  'placeholder': 'Product Image Alt Text',
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
        }


class ProductAttributeForm(forms.ModelForm):
    """Form for the ProductAttribute model."""
    class Meta:
        model = ProductAttribute
        fields = ['name', 'description',]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Product Attribute Name',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=500',
                    'placeholder': 'Product Attribute Description',
                }
            ),
        }


