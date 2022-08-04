"""Views for inventory app."""
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import (
    Category,
    Product,
    ProductImage,
    ProductAttributeValue,
    ProductInventory,
    Stock,
)


class ProductsListView(View):
    """View for the home page."""
    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        p = Paginator(Product.objects.all(), 35)
        page = request.GET.get('page')
        products = p.get_page(page)
        categories = Category.objects.all()
        context = {
            'products': products,
            'categories': categories,
        }
        categories = Category.objects.all()
        query = request.POST.get('search_query')
        if 'search_query' in request.GET:
            query = request.GET.get('search_query')
            if query == '' or query == 'All Categories':
                p = Paginator(Product.objects.all(), 35)
                page = request.GET.get('page')
                products = p.get_page(page)
                context = {
                    'products': products,
                    'categories': categories,
                }
                return render(
                    request,
                    'inventory/products_list.html',
                    context
                )
            else:
                products = Product.objects.filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query) |
                    Q(category__name__icontains=query) |
                    Q(brand__name__icontains=query) |
                    Q(tags__name__icontains=query)
                ).distinct()
                p = Paginator(products, 35)
                page = request.GET.get('page')
                products = p.get_page(page)
                context = {
                    'products': products,
                    'categories': categories,
                }
                return render(request, 'inventory/products_list.html', context)
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
            # Get the attribute for the product
            attr = product_inventory.product_type.product_type_attributes.all()
            for attribute in attr:
                # Get the attribute values for the product
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
        values_set_active_list = set()
        values_list = []
        for product_inventory_active in products_inventory_active:
            # Get the attribute for the active product
            product_inventory_active_stock = Stock.objects.filter(
                product_inventory=product_inventory_active
            )
            if product_inventory_active_stock:
                # Check if the product has stock
                attr = product_inventory_active.product_type.\
                    product_type_attributes.all()
                attribute_testing_set = set()
                for attribute in attr:
                    # Get the attribute values for the active product
                    attribute_testing_set.add(attribute.name)
                attribute_testing_set = sorted(attribute_testing_set)
                values = product_inventory_active.productattributevalues.all()
                product_inventory_active_values = {}
                for value in values:
                    # Get the attribute values for the active product
                    values_set_active.add(value.attributevalues)
                    values_set_active_list.add(
                        value.attributevalues.attribute_value
                    )
                    attribute_testing_set_list = list(attribute_testing_set)
                    selected_value = ProductAttributeValue.objects.filter(
                        attribute_value=value.attributevalues
                    )
                    for s_v in selected_value:
                        for attribute in attribute_testing_set_list:
                            # Check if the attribute is in the attr set list
                            if str(attribute) == str(
                                s_v.product_attribute
                            ):
                                product_inventory_active_values[
                                    attribute
                                ] = s_v.attribute_value
                # Get stock for the active product
                product_inventory_active_stock_units = Stock.objects.get(
                    product_inventory=product_inventory_active
                ).units
                product_inventory_active_values[
                    'Quantity'
                ] = product_inventory_active_stock_units
                #  get sale price for the active product
                product_inventory_active_sale_price = (
                    product_inventory_active.sale_price
                )
                # convert decimal to string
                product_inventory_active_sale_price = str(
                    product_inventory_active_sale_price
                )
                product_inventory_active_values[
                    'Price'
                ] = product_inventory_active_sale_price
                # Get the id of the active product
                product_inventory_active_id = product_inventory_active.id
                product_inventory_active_values[
                    'id'
                ] = product_inventory_active_id
                values_list.append(product_inventory_active_values)
        values_set_active_list = list(values_set_active_list)
        context = {
            'product': product,
            'active_images': active_images,
            'products_inventory': products_inventory,
            'attributes_set': attributes_set,
            'values_set': values_set,
            'attribute_values_dict': attribute_values_dict,
            'values_set_active': values_set_active,
            'values_set_active_list': values_set_active_list,
            'values_list': values_list,
        }
        return render(request, 'inventory/product_detail.html', context)
