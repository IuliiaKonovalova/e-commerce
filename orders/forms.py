"""Order form"""
from django import forms
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    """Form for Order Model"""
    class Meta:
        model = Order
        fields = [
            'full_name',
            'email',
            'phone',
            'address1',
            'address2',
            'city',
            'county_region_state',
            'country',
            'zip_code',
            'total_paid',
            'billing_status',
            'status',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address1': forms.TextInput(attrs={'class': 'form-control'}),
            'address2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'county_region_state': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'total_paid': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_status': forms.CheckboxInput(),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class OrderItemForm(forms.ModelForm):
    """Form for OrderItem Model"""
    class Meta:
        model = OrderItem
        fields = [
            'order',
            'product_inventory',
            'quantity',
        ]
        widgets = {
            'order': forms.HiddenInput(),
            'product_inventory': forms.HiddenInput(),
            'quantity': forms.TextInput(attrs={'class': 'form-control'}),
        }
