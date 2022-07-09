"""Veiws for the personnel app."""
from decimal import Decimal
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect, reverse
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
    CategoryForm,
    BrandForm,
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
                context = {
                    'product': product,
                    'active_images': active_images,
                    'get_all_images': get_all_images,
                    'active_now_promotions': active_now_promotions,
                    'product_inventory_in_promo_now': (
                        product_inventory_in_promo_now
                    ),
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


class EditProductView(View):
    """View for the edit product page."""

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
                product = get_object_or_404(Product, id=kwargs['pk'])
                form = ProductForm(instance=product)
                context = {
                    'form': form,
                    'product': product,
                }
                return render(
                    request,
                    'personnel/edit_product.html',
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
                product = get_object_or_404(Product, id=kwargs['pk'])
                form = ProductForm(request.POST, instance=product)
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
                        'personnel/edit_product.html',
                        {
                            'form': form,
                            'product': product,
                        }
                    )
        else:
            return render(
                request,
                'account/login.html',
            )


class DeleteProductView(View):
    """View for the delete product page."""

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
                product = get_object_or_404(Product, id=kwargs['pk'])
                context = {
                    'product': product,
                }
                return render(
                    request,
                    'personnel/delete_product.html',
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
                product = get_object_or_404(Product, id=kwargs['pk'])
                product.delete()
                return HttpResponseRedirect(
                    '/personnel/products_table/'
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


class ProductInventoryDetailsView(View):
    """View for the product inventory details page."""

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
                product_id = kwargs.get('pk')
                product_inventory_id = kwargs.get('inventory_pk')
                product_inventory = ProductInventory.objects.get(
                    id=product_inventory_id,
                )
                product = Product.objects.get(id=product_id)
                # promotions active now
                promotions = Promotion.objects.all().filter(active=True)
                active_now_promotions = []
                for promotion in promotions:
                    if promotion.is_active_now():
                        active_now_promotions.append(promotion)
                inPromoNow = False
                for promo in active_now_promotions:
                    promo_units = promo.products_inventory_in_promotion.all()
                    if product_inventory in promo_units:
                        inPromoNow = True
                stock_inconsistency = Stock.get_units_inconsistent()
                return render(
                    request,
                    'personnel/product_inventory_details.html',
                    {
                        'product': product,
                        'inventory': product_inventory,
                        'inPromoNow': inPromoNow,
                        'stock_inconsistency': stock_inconsistency,
                    }
                )
        else:
            return render(
                request,
                'account/login.html',
            )


class AddProductInventoryDetailsView(View):
    """View for the add product inventory details page."""

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
                product_id = kwargs.get('pk')
                product = Product.objects.get(id=product_id)
                # get all ProductType
                product_types = ProductType.objects.all()
                return render(
                    request,
                    'personnel/add_product_inventory_details.html',
                    {
                        'product': product,
                        'product_types': product_types,
                    }
                )
        else:
            return render(
                request,
                'account/login.html',
            )


class GetTypeAttributeAJAXView(View):
    """View for the get type attribute page."""

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
                    type_id = request.POST.get('type_id')
                    type_attribute = ProductType.objects.get(id=type_id)
                    all_attr = type_attribute.get_product_type_attributes()
                    attributes_set = set()
                    attribute_values_dict = {}
                    for attribute in all_attr:
                        # Get the attribute values for the product
                        attributes_set.add(attribute)
                        attribute_values_set = set()
                        attr_values = ProductAttributeValue.objects.filter(
                            product_attribute=attribute,
                        )
                        values_list = []
                        for attr_value in attr_values:
                            values_list.append(attr_value.attribute_value)
                        attribute_values_set.add(attr_value)
                        attribute_values_dict[attribute.name] = values_list
                    return JsonResponse(
                        {
                            'success': True,
                            'attribute_values_dict': attribute_values_dict,
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


class ProductInventoryCreateAJAXView(View):
    """View for the add product inventory details page."""

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
                    sku = request.POST.get('sku')
                    upc = request.POST.get('upc')
                    product = request.POST.get('product')
                    product_obj = Product.objects.get(id=product)
                    product_type = request.POST.get('product_type')
                    product_type_obj = ProductType.objects.get(id=product_type)
                    attribute_values = request.POST.get('attribute_values')
                    # attribute_values convert to dictionary
                    attribute_values_dict = json.loads(attribute_values)
                    retail_price = Decimal(request.POST.get('retail_price'))
                    store_price = Decimal(request.POST.get('store_price'))
                    sale_price = Decimal(request.POST.get('sale_price'))
                    weight = request.POST.get('weight')
                    is_active = request.POST.get('active') == 'true'
                    try:
                        product_inventory = ProductInventory.objects.create(
                            sku=sku,
                            upc=upc,
                            product=product_obj,
                            product_type=product_type_obj,
                            retail_price=retail_price,
                            store_price=store_price,
                            sale_price=sale_price,
                            weight=weight,
                            is_active=is_active,
                        )
                        product_inventory.save()
                        for attr_value in attribute_values_dict:
                            attr_obj = ProductAttribute.objects.get(
                                name=attr_value,
                            )
                            attr_value_obj = ProductAttributeValue.objects.get(
                                product_attribute=attr_obj,
                                attribute_value=attribute_values_dict[
                                    attr_value
                                ],
                            )
                            product_inventory.attribute_values.add(
                                attr_value_obj
                            )
                            product_inventory.save()
                        success_message = (
                            'Product inventory added successfully'
                        )
                        return JsonResponse(
                            {
                                'success': True,
                                'success_message': success_message,
                            }
                        )
                    except Exception as e:
                        error_message = (
                            'Error adding product inventory. '
                            'Error: '
                            f'{e}'
                            ' Please check unique fields.'
                        )
                        return JsonResponse(
                            {
                                'success': True,
                                'error_message': error_message,
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


class EditProductInventoryView(View):
    """View for the edit product inventory page."""

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
                product_inventory_id = kwargs.get('inventory_pk')
                inventory = ProductInventory.objects.get(
                    id=product_inventory_id,
                )
                pk = inventory.product.id
                product_types = ProductType.objects.all()
                inventory_type = inventory.product_type
                return render(
                    request,
                    'personnel/edit_product_inventory.html',
                    {
                        'inventory': inventory,
                        'product_types': product_types,
                        'pk': pk,
                        'inventory_type': inventory_type,
                    }
                )
        else:
            return render(
                request,
                'account/login.html',
            )


class UpdateProductInventoryAJAXView(View):
    """View for the update product inventory page."""

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
                    product_inventory_id = request.POST.get('inventory_id')
                    inventory = ProductInventory.objects.get(
                        id=product_inventory_id,
                    )
                    sku = request.POST.get('sku')
                    upc = request.POST.get('upc')
                    product = request.POST.get('product')
                    product_obj = Product.objects.get(id=product)
                    product_type = request.POST.get('product_type')
                    product_type_obj = ProductType.objects.get(id=product_type)
                    attribute_values = request.POST.get('attribute_values')
                    # attribute_values convert to dictionary
                    attribute_values_dict = json.loads(attribute_values)
                    retail_price = Decimal(request.POST.get('retail_price'))
                    store_price = Decimal(request.POST.get('store_price'))
                    sale_price = Decimal(request.POST.get('sale_price'))
                    weight = request.POST.get('weight')
                    is_active = request.POST.get('active') == 'true'
                    try:
                        inventory.sku = sku
                        inventory.upc = upc
                        inventory.product = product_obj
                        inventory.product_type = product_type_obj
                        inventory.retail_price = retail_price
                        inventory.store_price = store_price
                        inventory.sale_price = sale_price
                        inventory.weight = weight
                        inventory.is_active = is_active
                        inventory.save()
                        #  remove all from inventory.attribute_values
                        inventory.attribute_values.clear()
                        for attr_value in attribute_values_dict:
                            attr_obj = ProductAttribute.objects.get(
                                name=attr_value,
                            )
                            attr_value_obj = ProductAttributeValue.objects.get(
                                product_attribute=attr_obj,
                                attribute_value=attribute_values_dict[
                                    attr_value
                                ],
                            )
                            inventory.attribute_values.add(
                                attr_value_obj
                            )
                            inventory.save()
                        success_message = (
                            'Product inventory updated successfully'
                        )
                        return JsonResponse(
                            {
                                'success': True,
                                'success_message': success_message,
                            }
                        )
                    except Exception as e:
                        error_message = (
                            'Error updating product inventory. '
                            'Error: '
                            f'{e}'
                            ' Please check unique fields.'
                        )
                        return JsonResponse(
                            {
                                'success': True,
                                'error_message': error_message,
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


class DeleteProductInventoryView(View):
    """View for the delete product inventory page."""

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
                inventory = get_object_or_404(
                    ProductInventory,
                    id=kwargs['inventory_pk']
                )
                pk = inventory.product.id
                return render(
                    request,
                    'personnel/delete_product_inventory.html',
                    {
                        'inventory': inventory,
                        'pk': pk,
                    }
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
                inventory = get_object_or_404(
                    ProductInventory,
                    id=kwargs['inventory_pk']
                )
                inventory.delete()
                pk = inventory.product.id
                return HttpResponseRedirect(
                    '/personnel/product/{}/'.format(
                        pk
                    )
                )
        else:
            return render(
                request,
                'account/login.html',
            )


class ProductInventoriesTableView(View):
    """View for the product inventories table page."""

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
                p = Paginator(ProductInventory.objects.all(), 10)
                page = request.GET.get('page')
                inventories = p.get_page(page)
                # promotions active now
                promotions = Promotion.objects.all().filter(active=True)
                active_now_promotions = []
                for promotion in promotions:
                    if promotion.is_active_now():
                        active_now_promotions.append(promotion)
                context = {
                    'inventories': inventories,
                    'active_now_promotions': active_now_promotions,
                }
                return render(
                    request,
                    'personnel/product_inventories_table.html',
                    context,
                )
        else:
            return render(
                request,
                'account/login.html',
            )


class CategoriesTableView(View):
    """View for the categories table page."""
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
                categories = Category.objects.all()
                context = {
                    'categories': categories,
                }
                return render(
                    request,
                    'personnel/categories_table.html',
                    context,
                )
        else:
            return render(
                request,
                'account/login.html',
            )


class AddCategoryView(View):
    """View for the add category page."""
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
                form = CategoryForm(request.POST)
                return render(
                    request,
                    'personnel/add_category.html',
                    {'form': form},
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
                form = CategoryForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(
                        '/personnel/categories_table/'
                    )
                else:
                    return render(
                        request,
                        'personnel/add_category.html',
                        {'form': form},
                    )
        else:
            return render(
                request,
                'account/login.html',
            )


class EditCategoryView(View):
    """View for the edit category page."""
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
                category = get_object_or_404(
                    Category,
                    id=kwargs['category_pk']
                )
                form = CategoryForm(instance=category)
                return render(
                    request,
                    'personnel/edit_category.html',
                    {'form': form, 'category': category},
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
                category = get_object_or_404(
                    Category,
                    id=kwargs['category_pk']
                )
                form = CategoryForm(request.POST, instance=category)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(
                        '/personnel/categories_table/'
                    )
                else:
                    return render(
                        request,
                        'personnel/edit_category.html',
                        {'form': form, 'category': category},
                    )
        else:
            return render(
                request,
                'account/login.html',
            )


class DeleteCategoryView(View):
    """View for the delete category page."""
    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        if request.user.is_authenticated:
            # Check if user is a customer
            if request.user.profile.role.id == 3:
                category = get_object_or_404(
                    Category,
                    id=kwargs['category_pk']
                )
                return render(
                    request,
                    'personnel/delete_category.html',
                    {'category': category},
                )
            else:
                return render(
                    request,
                    'profiles/access_denied.html',
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
            if request.user.profile.role.id == 3:
                category = get_object_or_404(
                    Category,
                    id=kwargs['category_pk']
                )
                category.delete()
                return HttpResponseRedirect(
                    '/personnel/categories_table/'
                )
            else:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
        else:
            return render(
                request,
                'account/login.html',
            )


class BrandsTableView(View):
    """View for the brands table page."""
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
                p  = Paginator(Brand.objects.all(), 25)
                page = request.GET.get('page')
                brands = p.get_page(page)
                context = {
                    'brands': brands,
                }
                return render(
                    request,
                    'personnel/brands_table.html',
                    context,
                )
        else:
            return render(
                request,
                'account/login.html',
            )


class BrandDetailView(View):
    """View for the brand detail page."""
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
                brand = get_object_or_404(
                    Brand,
                    id=kwargs['brand_pk']
                )
                return render(
                    request,
                    'personnel/brand_detail.html',
                    {'brand': brand},
                )
        else:
            return render(
                request,
                'account/login.html',
            )


class AddBrandView(View):
    """View for the add brand page."""
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
                form = BrandForm()
                return render(
                    request,
                    'personnel/add_brand.html',
                    {'form': form},
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
                form = BrandForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(
                        '/personnel/brands_table/'
                    )
                else:
                    return render(
                        request,
                        'personnel/add_brand.html',
                        {'form': form},
                    )
        else:
            return render(
                request,
                'account/login.html',
            )


class EditBrandView(View):
    """View for the edit brand page."""
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
                brand = get_object_or_404(
                    Brand,
                    id=kwargs['brand_pk']
                )
                form = BrandForm(instance=brand)
                return render(
                    request,
                    'personnel/edit_brand.html',
                    {'form': form, 'brand': brand},
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
                brand = get_object_or_404(
                    Brand,
                    id=kwargs['brand_pk']
                )
                form = BrandForm(request.POST, instance=brand)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(
                        '/personnel/brand/{}/'.format(brand.id)
                    )
                else:
                    return render(
                        request,
                        'personnel/edit_brand.html',
                        {'form': form, 'brand': brand},
                    )
        else:
            return render(
                request,
                'account/login.html',
            )