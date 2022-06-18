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
            attr = product_inventory.product_type.product_type_attributes.all()
            for attribute in attr:
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


class ProductAttributeAJAXView(View):
    """View for the product attribute AJAX."""
    def post(self, request, *args, **kwargs):
        """Handle GET requests."""
        # product_id = kwargs['pk']
        # # get products_inventory
        # products_inventory_active = ProductInventory.objects.filter(
        #     product=product_id,
        #     is_active=True
        # )
        # attributes_set_active = set()
        # values_set_active = set()
        # attribute_values_dict_active = {}
        # for product_inventory_active in products_inventory_active:
        #     attributes_active = product_inventory_active.\
        #         product_type.product_type_attributes.all()
        #     for attribute in attributes_active:
        #         attributes_set_active.add(attribute)
        #         # attribute_values_set_active = set()
        #         attribute_value_active = ProductAttributeValue.objects.filter(
        #             product_attribute=attribute,
        #         )
        #         # attribute_values_set_active.add(attribute_value)
        #         attribute_values_dict_active[
        #             attribute
        #         ] = attribute_value_active
        #     values = product_inventory_active.productattributevalues.all()
        #     for value in values:
        #         values_set_active.add(value.attributevalues)
        # print(attribute_values_dict_active)
        if request.is_ajax():
            value = request.GET.get('value')
            product_id = request.GET.get('product_id')
            attribute = request.GET.get('attribute')


