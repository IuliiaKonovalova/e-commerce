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
    ProductAttributeValues,
    ProductTypeAttribute,
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
        products_inventory = ProductInventory.objects.filter(
            product=product
        )
        attributes_set = set()
        values_set = set()
        attribute_values_dict = {}
        for product_inventory in products_inventory:
            attributes = product_inventory.product_type.product_type_attributes.all()
            for attribute in attributes:
                attributes_set.add(attribute)
                attribute_values_set = set()
                attribute_value = ProductAttributeValue.objects.filter(
                    product_attribute=attribute,
                )
                attribute_values_set.add(attribute_value)
                attribute_values_dict[attribute] = attribute_value
            values = product_inventory.productattributevalues.all()
            for value in values:
                values_set.add(value.attributevalues)
        products_inventory_active = ProductInventory.objects.filter(
            product=product,
            is_active=True
        )
        attributes_set_active = set()
        values_set_active = set()
        for product_inventory_active in products_inventory_active:
            values = product_inventory_active.productattributevalues.all()
            for value in values:
                values_set_active.add(value.attributevalues)


        context = {
            'product': product,
            'active_images': active_images,
            'products_inventory': products_inventory,
            'attributes_set': attributes_set,
            'values_set': values_set,
            'attribute_values_dict': attribute_values_dict,
            'values_set_active': values_set_active,
        }
        return render(request, 'inventory/product_detail.html', context)


