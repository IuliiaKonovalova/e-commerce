"""Forms for the inventory app."""
from django import forms
from inventory.models import (
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
        fields = ['name', 'is_active']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Category Name',
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
        fields = ['name', 'is_active']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Tag Name',
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
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Brand Name',
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
                }
            ),
            'tags': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'title': 'select tags',
                }
            ),
            'brand': forms.Select(
                attrs={
                    'class': 'form-control',
                    'title': 'select a brand',
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
        fields = ['name', 'description']
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


class ProductTypeForm(forms.ModelForm):
    """Form for the ProductType model."""
    class Meta:
        model = ProductType
        fields = [
            'name',
            'product_type_attributes',
            'description',
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Product Type Name',
                }
            ),
            'product_type_attributes': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'title': 'select attributes',
                    'required': False,
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=500',
                    'placeholder': 'Product Type Description',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_type_attributes'].required = False


class ProductAttributeValueForm(forms.ModelForm):
    """Form for the ProductAttributeValue model."""
    class Meta:
        model = ProductAttributeValue
        fields = ['product_attribute', 'attribute_value']
        widgets = {
            'product_attribute': forms.Select(
                attrs={
                    'class': 'form-control',
                    'title': 'select an attribute',
                }
            ),
            'attribute_value': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Product Attribute Value',
                }
            ),
        }


class ProductInventoryForm(forms.ModelForm):
    """Form for the ProductInventory model."""
    class Meta:
        model = ProductInventory
        fields = [
            'sku',
            'upc',
            'product',
            'product_type',
            'attribute_values',
            'retail_price',
            'store_price',
            'sale_price',
            'weight',
            'is_active',
        ]
        retail_price = forms.DecimalField()
        store_price = forms.DecimalField()
        sale_price = forms.DecimalField()
        widgets = {
            'sku': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=50',
                    'placeholder': 'Product SKU',
                }
            ),
            'upc': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'title': 'max_length=12',
                    'placeholder': 'Product UPC',
                }
            ),
            'product': forms.Select(
                attrs={
                    'class': 'form-control',
                    'title': 'select a product',
                    'placeholder': 'Product',
                }
            ),
            'product_type': forms.Select(
                attrs={
                    'class': 'form-control',
                    'title': 'select a product type',
                    'placeholder': 'Product Type',
                }
            ),
            'attribute_values': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'title': 'select attribute values',
                    'placeholder': 'Attribute Values',
                }
            ),
            'weight': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'title': 'Product Weight in grams',
                    'placeholder': 'Product Weight',
                    'step': '0.1',
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
        }


class StockForm(forms.ModelForm):
    """Form for the Stock model."""
    class Meta:
        model = Stock
        fields = [
            'last_checked',
            'units_variable',
            'units',
            'units_sold',
        ]
        widgets = {
            'last_checked': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'title': 'last checked',
                    'placeholder': 'Last Checked',
                }
            ),
            'units_variable': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'title': 'units variable',
                    'placeholder': 'Units Variable',
                }
            ),
            'units': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'title': 'units',
                    'placeholder': 'Units',
                }
            ),
            'units_sold': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'title': 'units sold',
                    'placeholder': 'Units Sold',
                }
            ),
        }
