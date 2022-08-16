"""Views for email_notifications app."""
import json
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from email_notifications.forms import EmailNewsNotificationForm
from inventory.models import (
    Product,
    ProductAttribute,
    ProductAttributeValue,
    ProductInventory,
    Stock,
)
from email_notifications.models import (
    StockEmailNotification,
)


class EmailStockNotificationFormAJAX(View):
    """View for the email stock notification form AJAX."""
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.is_ajax():
                data = request.POST['data']
                data_dict = json.loads(data)
                product_id = data_dict['id']
                product_options = data_dict['options']
                requested_quantity = int(data_dict['quantity'])
                attribute_values_ids = []
                target = None
                # loop through the dictionary product_options
                for key, value in product_options.items():
                    # get the product attribute
                    product_attribute_id = ProductAttribute.objects.get(
                        name=key
                    ).id
                    # get the product attribute value
                    product_attribute_value_id = ProductAttributeValue.objects\
                        .get(
                            product_attribute=product_attribute_id,
                            attribute_value=value
                        ).id
                    attribute_values_ids.append(product_attribute_value_id)
                # get all product inventory by product_id
                product_inventories = ProductInventory.objects.filter(
                    product=product_id
                )
                # check all product inventories of this product
                for product_inventory in product_inventories:
                    product_attribute_values = product_inventory.\
                        get_attribute_values()
                    product_attribute_values_ids = [
                        product_attribute_value.id for
                        product_attribute_value in product_attribute_values
                    ]
                    # sort  attribute_values_ids
                    attribute_values_ids.sort()
                    product_attribute_values_ids.sort()
                    # check if we found the product inventory
                    if attribute_values_ids == product_attribute_values_ids:
                        target = product_inventory
                alert_message = ''
                # check if target is not None
                if target is not None:
                    # check stock exists
                    if Stock.objects.filter(product_inventory=target).exists():
                        if target.stock.units > requested_quantity:
                            alert_message = (
                                'We have enough stock! You can buy it now!'
                            )
                            return JsonResponse(
                                {
                                    'success': True,
                                    'alert_message': alert_message,
                                }
                            )
                # get product by product_id
                product = get_object_or_404(Product, id=product_id)
                stock_email_notification_this = StockEmailNotification.\
                    objects.create(
                        user=request.user,
                        requested_product=product,
                        requested_quantity=requested_quantity,
                        answer_sent=False,
                    )
                for attribute_value_id in attribute_values_ids:
                    # get the product attribute value
                    product_attribute_value = get_object_or_404(
                        ProductAttributeValue,
                        id=attribute_value_id
                    )
                    # add the product attribute value to the object
                    stock_email_notification_this.\
                        requested_attributes_values.add(
                            product_attribute_value
                        )
                alert_message = (
                    'We will notify you when we have enough stock.'
                )
                return JsonResponse(
                    {
                        'success': True,
                        'alert_message': alert_message,
                    }
                )
            else:
                return JsonResponse({'success': False})

        else:
            return render(
                request,
                'account/login.html',
            )


class PromoEmailCreateView(View):
    """Send email to the user for promotion or news"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                form = EmailNewsNotificationForm()
                return render(
                    request,
                    'email_notifications/promo_email_create.html',
                    {
                        'form': form,
                    }
                )
        else:
            return render(
                request,
                'account/login.html',
            )

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                form = EmailNewsNotificationForm(request.POST)
                if form.is_valid():
                    form.save()
                    return render(
                        request,
                        'promotions/promotions_list.html',
                    )
                else:
                    return render(
                        request,
                        'email_notifications/promo_email_create.html',
                        {
                            'form': form,
                            'success': False,
                        }
                    )
        else:
            return render(
                request,
                'account/login.html',
            )


class StockRequestsListView(View):
    """List of stock requests"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                stock_requests = StockEmailNotification.objects.filter(
                    answer_sent=False
                )
                # get all Product from stock_requests
                products = set()
                for stock_request in stock_requests:
                    products.add(stock_request.requested_product.name)
                context = {
                    'stock_requests': stock_requests,
                    'products': products,
                }
                if 'search_query' in request.GET:
                    query = request.GET.get('search_query')
                    if query == '':
                        return render(
                            request,
                            'email_notifications/stock_requests_list.html',
                            context
                        )
                    else:
                        stock_requests = stock_requests.filter(
                            Q(requested_product__name__icontains=query) |
                            Q(user__username__icontains=query)
                        )
                        context['stock_requests'] = stock_requests
                        return render(
                            request,
                            'email_notifications/stock_requests_list.html',
                            context
                        )
                return render(
                    request,
                    'email_notifications/stock_requests_list.html',
                    context,
                )
        else:
            return render(
                request,
                'account/login.html',
            )
