from django.views import View
from django.shortcuts import render
from .models import (
    Category,
    Tag,
    Brand,
    Product,
    ProductImage,
    ProductType,
    ProductAttribute,
    ProductAttributeValue,
    ProductInventory,
    Stock,
)
from django.contrib.auth.decorators import login_required


class ProductsListView(View):
    """View for the home page."""
    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        products = Product.objects.all()
        context = {
            'products': products,
        }
        return render(request, 'inventory/products_list.html', context)


class ProductDetailView(View):
    """View for the product detail page."""
    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        product = Product.objects.get(id=kwargs['pk'])
        active_images = ProductImage.objects.filter(
            product=product,
            is_active=True
        )
        context = {
            'product': product,
            'active_images': active_images,
        }
        return render(request, 'inventory/product_detail.html', context)
