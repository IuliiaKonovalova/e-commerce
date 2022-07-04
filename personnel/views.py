"""Veiws for the personnel app."""
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
import json
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
from .forms import (
    ProductForm,
)


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
                    if promotion.is_active_now():
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
                active_now_promotions = []
                for promotion in promotions:
                    if promotion.is_active_now():
                        active_now_promotions.append(promotion)
                product_inventory_in_promo_now = set()
                # pi
                products_inventory = ProductInventory.objects.filter(
                    product=product
                )
                for promotion in active_now_promotions:
                    pi = promotion.products_inventory_in_promotion.all()
                    for p in pi:
                        if p in products_inventory:
                            product_inventory_in_promo_now.add(p)
                attributes_set = set()
                values_set = set()
                attribute_values_dict = {}
                for product_inventory in products_inventory:
                    # Get the attribute for the product
                    attr = product_inventory.product_type.\
                        product_type_attributes.all()
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
                    'product_inventory_in_promo_now': (
                        product_inventory_in_promo_now
                    ),
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


class AddProductView(View):
    """View for the add product page."""
    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        if request.user.is_authenticated:
            # Check if user is a customer
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                form = ProductForm()
                context = {
                    'form': form,
                }
                return render(
                    request,
                    'personnel/add_product.html',
                    context
                )
        else:
            return render(
                request,
                'account/login.html',
            )

    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
        if request.user.is_authenticated:
            # Check if user is a customer
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                form = ProductForm(request.POST)
                if form.is_valid():
                    product = form.save(commit=False)
                    tags = form.cleaned_data['tags']
                    product.save()
                    product.tags.set(tags)
                    product.save()
                    # get pk of this product
                    product_pk = product.id
                    return HttpResponseRedirect(
                        '/personnel/product/{}'.format(product_pk)
                    )
                else:
                    return render(
                        request,
                        'personnel/add_product.html',
                        {
                            'form': form,
                        }
                    )
        else:
            return render(
                request,
                'account/login.html',
            )


class AddImageToProductAJAXView(View):
    """View for the add image to product page."""
    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
        if request.user.is_authenticated:
            # Check if user is a customer
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                if request.is_ajax():
                    product = request.POST.get('product_id')
                    image = request.FILES.get('image')
                    alt_text = request.POST.get('alt_text')
                    default_image = request.POST.get('default_image') == 'true'
                    is_active = request.POST.get('is_active') == 'true'
                    product_object = Product.objects.get(id=product)
                    # create a new product image
                    new_image = ProductImage.objects.create(
                        product=product_object,
                        image=image,
                        alt_text=alt_text,
                        default_image=default_image,
                        is_active=is_active,
                    )
                    new_image.save()
                    # get the new image pk
                    new_image_pk = new_image.id
                    # new_image_image = new_image.image
                    new_image_alt_text = new_image.alt_text
                    new_image_default_image = new_image.default_image
                    new_image_is_active = new_image.is_active
                    new_image_image_url = new_image.image_url
                    return JsonResponse(
                        {
                            'success': True,
                            'new_image_pk': new_image_pk,
                            # 'new_image_image': new_image_image,
                            'new_image_alt_text': new_image_alt_text,
                            'new_image_default_image': new_image_default_image,
                            'new_image_is_active': new_image_is_active,
                            'new_image_image_url': new_image_image_url,
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'success': False,
                        }
                    )
        else:
            return render(
                request,
                'account/login.html',
            )


class EditImageToProductAJAXView(View):
    """View for the edit image to product page."""
    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
        if request.user.is_authenticated:
            # Check if user is a customer
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                if request.is_ajax():
                    image_id = request.POST.get('image_id')
                    product = request.POST.get('product_id')
                    image = request.FILES.get('image')
                    alt_text = request.POST.get('alt_text')
                    default_image = request.POST.get('default_image') == 'true'
                    is_active = request.POST.get('is_active') == 'true'
                    updated_image = ProductImage.objects.get(id=image_id)
                    if image:
                        updated_image.image = image
                    # update product_object
                    updated_image.alt_text = alt_text
                    updated_image.default_image = default_image
                    updated_image.is_active = is_active
                    updated_image.save()
                    # get data:
                    image_id = image_id
                    update_image = ProductImage.objects.get(id=image_id)
                    update_alt_text = update_image.alt_text
                    update_default_image = update_image.default_image
                    update_is_active = update_image.is_active
                    update_image_url = update_image.image_url
                    return JsonResponse(
                        {
                            'success': True,
                            'image_id': image_id,
                            # 'new_image_image': new_image_image,
                            'update_alt_text': update_alt_text,
                            'update_default_image': update_default_image,
                            'update_is_active': update_is_active,
                            'update_image_url': update_image_url,
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'success': False,
                        }
                    )
        else:
            return render(
                request,
                'account/login.html',
            )


class DeleteImageToProductAJAXView(View):
    """View for the delete image to product page."""
    def post(self, request, *args, **kwargs):
        """Handle POST requests."""
        if request.user.is_authenticated:
            # Check if user is a customer
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                if request.is_ajax():
                    image_id = request.POST.get('image_id')
                    updated_image = ProductImage.objects.get(id=image_id)
                    updated_image.delete()
                    return JsonResponse(
                        {
                            'success': True,
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            'success': False,
                        }
                    )
        else:
            return render(
                request,
                'account/login.html',
            )
