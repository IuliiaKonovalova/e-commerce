"""Veiws for the personnel app."""
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from inventory.models import (
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
from promotions.models import Promotion


class ProductsTableView(View):
    """View for the home page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if user is a admin
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                p = Paginator(Product.objects.all(), 3)
                page = request.GET.get('page')
                products = p.get_page(page)
                promotions = Promotion.objects.all().filter(active=True)
                active_now_promotions = []
                for promotion in promotions:
                    if promotion.is_active_now() == True:
                        active_now_promotions.append(promotion)
                context = {
                    'products': products,
                    'promotions': promotions,
                    'active_now_promotions': active_now_promotions,
                }
                return render(
                    request,
                    'personnel/products_table.html',
                    context
                )
        else:
            return render(
                request,
                'account/login.html',
            )


class ProductFullDetailView(View):
    """View for the product detail page."""
    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        if request.user.is_authenticated:
            # Check if user is a admin
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                product = Product.objects.get(id=kwargs['pk'])
                active_images = ProductImage.objects.filter(
                    product=product,
                    is_active=True
                )
                get_all_images = ProductImage.objects.filter(
                    product=product
                )

                # promotions active now
                promotions = Promotion.objects.all().filter(active=True)
                print(promotions)
                active_now_promotions = []
                for promotion in promotions:
                    if promotion.is_active_now() == True:
                        print(promotion)
                        active_now_promotions.append(promotion)
                print(active_now_promotions)
                product_inventory_in_promo_now = set()

                # pi
                products_inventory = ProductInventory.objects.filter(
                    product=product
                )
                for promotion in active_now_promotions:
                    pi = promotion.products_inventory_in_promotion.all()
                    print(pi)
                    for p in pi:
                        print(p)
                        if p in products_inventory:
                            product_inventory_in_promo_now.add(p)
                print(product_inventory_in_promo_now)
                
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
                    values_set.add(values)
                context = {
                    'product': product,
                    'active_images': active_images,
                    'get_all_images': get_all_images,
                    'active_now_promotions': active_now_promotions,
                    'product_inventory_in_promo_now': product_inventory_in_promo_now,
                    'attributes_set': attributes_set,
                    'values_set': values_set,
                    'attribute_values_dict': attribute_values_dict,
                }
                return render(
                    request,
                    'personnel/product_detail_full.html',
                    context
                )
        else:
            return render(
                request,
                'account/login.html',
            )