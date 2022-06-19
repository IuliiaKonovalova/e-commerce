from django.views import View
from django.shortcuts import render, get_object_or_404 
from django.http import JsonResponse, HttpResponseRedirect
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
        values_list = []
        for product_inventory_active in products_inventory_active:
            product_inventory_active_stock = Stock.objects.filter(
                product_inventory=product_inventory_active
            )
            print(product_inventory_active_stock)
            if product_inventory_active_stock:
                attr = product_inventory_active.product_type.product_type_attributes.all()
                attribute_testing_set = set()
                for attribute in attr:
                    attribute_testing_set.add(attribute.name)
                attribute_testing_set = sorted(attribute_testing_set)
                values = product_inventory_active.productattributevalues.all()
                product_inventory_active_values = {}
                for value in values:

                    values_set_active.add(value.attributevalues)
                    selected_value = ProductAttributeValue.objects.get(
                        attribute_value = value.attributevalues
                    )
                    attribute_testing_set_list = list(attribute_testing_set)
                    for attribute in attribute_testing_set_list:
                        if str(attribute) == str(selected_value.product_attribute):
                            product_inventory_active_values[attribute] = selected_value.attribute_value
                            # product_inventory_active_values.append(
                            #     "{}: {}".format(attribute, selected_value.attribute_value)
                            # )
                product_inventory_active_stock_units = Stock.objects.get(
                    product_inventory=product_inventory_active
                ).units
                # product_inventory_active_values.append(
                #     "Quantity: {}".format(
                #         product_inventory_active_stock_units
                #     )
                # )
                product_inventory_active_values['Quantity'] = product_inventory_active_stock_units
                # product_inventory_active_values transform to dict
                # product_inventory_active_values = dict(
                #     product_inventory_active_values
                # )
                values_list.append(product_inventory_active_values)
        print('values_list', values_list)
        context = {
            'product': product,
            'active_images': active_images,
            'products_inventory': products_inventory,
            'attributes_set': attributes_set,
            'values_set': values_set,
            'attribute_values_dict': attribute_values_dict,
            'values_set_active': values_set_active,
            'values_list': values_list,
        }
        return render(request, 'inventory/product_detail.html', context)


class ProductAttributeAJAXView(View):
    """View for the product attribute AJAX."""
    def post(self, request, *args, **kwargs):
        """Handle GET requests."""
        if request.is_ajax():
            value = request.POST.get('value')
            product_id = request.POST.get('product_id')
            # address = get_object_or_404(Address, id=address_id)
            print(product_id)
            attribute = request.POST.get('attribute')
            print(attribute)
            products_inventory_active = ProductInventory.objects.filter(
                product=product_id,
                is_active=True,
            )
            print(products_inventory_active)
            print('huy')
            values_set_add = set()
            attribute_values_set = set()
            for product_inventory_active in products_inventory_active:
                sth = product_inventory_active.attribute_values.all()
                attr = product_inventory_active.product_type.product_type_attributes.all()
                for attribute in attr:
                    attribute_values_set.add(attribute)

                print("all_values")
                print(sth)
                # print(sth.filter(attributevalues__in='red'))
                selected_value = ProductAttributeValue.objects.get(
                    attribute_value = value
                )
                print(selected_value.id)
                print(selected_value.attribute_value)
                if selected_value in sth:
                    print('should be yellow')
                    print(value)
                    values_all = product_inventory_active.productattributevalues.all()
                    print(values_all)
                    for value1 in values_all:
                        print('this is value1')
                        print(value1)
                        print('this is value1.attributevalues')
                        print(value1.attributevalues)
                        if value1.attributevalues == selected_value:
                            print('should be yellow value')
                            continue
                        else:
                            values_set_add.add(value1.attributevalues.attribute_value)
                            print(values_set_add)
                else:
                    print('not yellow')
            print(values_set_add)
            # values_set_add to list
            values_set_add_list = list(values_set_add)
            print(values_set_add_list)
            return JsonResponse({'success': True, 'values_set_add_list': values_set_add_list,})
        else:
            return JsonResponse({'success': False})