"""Views for orders app."""
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db.models import Q
from inventory.models import ProductInventory

from reviews.models import Review
from .models import Order, OrderItem
from bag.contexts import bag_contents
from .forms import OrderForm, OrderItemForm


class OrdersView(View):
    """View for orders page."""

    def get(self, request):
        """Get method for orders page."""
        if request.user.is_authenticated:
            # Check if user is a admin
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                p = Paginator(Order.objects.all(), 25)
                page = request.GET.get('page')
                orders = p.get_page(page)
                context = {
                    'orders': orders,
                }
                if 'search_query' in request.GET:
                    query = request.GET.get('search_query')
                    if query == '':
                        p = Paginator(
                            Order.objects.all(),
                            25
                        )
                        page = request.GET.get('page')
                        orders = p.get_page(page)
                        context = {
                            'orders': orders,
                        }
                        return render(
                            request,
                            'orders/orders.html',
                            context
                        )
                    orders = Order.objects.filter(
                          Q(full_name__icontains=query) |
                          Q(email__icontains=query) |
                          Q(phone__icontains=query) |
                          Q(city__icontains=query) |
                          Q(county_region_state__icontains=query) |
                          Q(country__icontains=query) |
                          Q(status__icontains=query) |
                          Q(order_number__icontains=query) |
                          Q(order_key__icontains=query) |
                          Q(status__icontains=query)
                    )
                    p = Paginator(orders, 25)
                    page = request.GET.get('page')
                    orders = p.get_page(page)
                    context = {
                        'orders': orders,
                    }
                    return render(
                        request,
                        'orders/orders.html',
                        context
                    )
                return render(request, 'orders/orders.html', context)
        else:
            return render(
                request,
                'account/login.html',
            )


class OrderDetailsView(View):
    """View for order full page."""

    def get(self, request, *args, **kwargs):
        """Get method for order details page."""
        if request.user.is_authenticated:
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                order_id = kwargs['order_id']
                order = get_object_or_404(Order, id=order_id)
                order_items = OrderItem.objects.filter(order=order)
                context = {
                    'order': order,
                    'order_items': order_items,

                }
                return render(request, 'orders/order_details.html', context)
        else:
            return render(
                request,
                'account/login.html',
            )


class UpdateOrderStatusAJAXView(View):
    """
    View for updating order status with access only
    for admin and logistic manager
    """
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_role = request.user.profile.role.id
            if user_role == 3 or user_role == 4:
                if request.is_ajax():
                    order_id = request.POST.get('order_id')
                    order = get_object_or_404(Order, id=order_id)
                    order.status = request.POST.get('order_status')
                    order.save()
                    return JsonResponse(
                        {
                            'success': True,
                            'order_status': order.status,
                        },
                    )
                else:
                    return JsonResponse({'success': False})
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


class AddOrderAJAXView(View):
    """View for adding order AJAX."""
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.is_ajax():
                bag = bag_contents(request)
                promo_price = bag['promo_price']
                if promo_price and promo_price != 0:
                    total_final = promo_price
                else:
                    total_final = bag['total']
                user = request.user
                full_name = request.POST.get('full_name')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                address1 = request.POST.get('address1')
                address2 = request.POST.get('address2')
                country = request.POST.get('country')
                county_region_state = request.POST.get('county_region_state')
                city = request.POST.get('city')
                zip_code = request.POST.get('zip_code')
                order_key = request.POST.get('order_key')
                bag = bag_contents(request)
                total_paid = str(total_final)
                bag_items = bag['bag_items']
                if Order.objects.filter(order_key=order_key).exists():
                    pass
                else:
                    order = Order.objects.create(
                        user=user,
                        full_name=full_name,
                        email=email,
                        phone=phone,
                        address1=address1,
                        address2=address2,
                        country=country,
                        county_region_state=county_region_state,
                        city=city,
                        zip_code=zip_code,
                        order_key=order_key,
                        total_paid=total_paid,
                    )
                    for item in bag_items:
                        item = OrderItem.objects.create(
                            order=order,
                            product_inventory=item['product_inventory'],
                            quantity=item['quantity'],
                        )
                return JsonResponse({'success': True})
            return JsonResponse({'success': False})
        else:
            return render(
                request,
                'account/login.html',
            )


class EditOrderView(View):
    """View to edit order"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.role.id == 3:
                order = get_object_or_404(Order, id=kwargs['order_id'])
                form = OrderForm(instance=order)
                context = {
                    'form': form,
                    'order': order,
                }
                return render(request, 'orders/edit_order.html', context)
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
        if request.user.is_authenticated:
            if request.user.profile.role.id == 3:
                order = get_object_or_404(Order, id=kwargs['order_id'])
                form = OrderForm(request.POST, instance=order)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(
                        '/orders/order_details/{}'.format(order.id)
                    )
                context = {
                    'form': form,
                    'order': order,
                }
                return render(request, 'orders/edit_order.html', context)
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


class DeleteOrderView(View):
    """View to delete order"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.role.id == 3:
                order = get_object_or_404(Order, id=kwargs['order_id'])
                context = {
                    'order': order,
                }
                return render(request, 'orders/delete_order.html', context)
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
        if request.user.is_authenticated:
            if request.user.profile.role.id == 3:
                order = get_object_or_404(Order, id=kwargs['order_id'])
                order.delete()
                return HttpResponseRedirect('/orders/')
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


class EditOrderItemView(View):
    """View to edit order item"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.role.id == 3:
                order_item = get_object_or_404(
                    OrderItem,
                    id=kwargs['order_item_id']
                )
                # get product inventory
                product_inventory = get_object_or_404(
                    ProductInventory,
                    id=order_item.product_inventory.id
                )
                # get sale_price
                sale_price = product_inventory.sale_price
                # origin quantity
                origin_quantity = order_item.quantity
                # multiply sale_price and origin quantity
                total_price = sale_price * origin_quantity
                form = OrderItemForm(instance=order_item)
                context = {
                    'form': form,
                    'order_item': order_item,
                }
                return render(request, 'orders/edit_order_item.html', context)
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
        if request.user.is_authenticated:
            if request.user.profile.role.id == 3:
                order_item = get_object_or_404(
                    OrderItem,
                    id=kwargs['order_item_id']
                )
                # get product inventory
                product_inventory = get_object_or_404(
                    ProductInventory,
                    id=order_item.product_inventory.id
                )
                # get sale_price
                sale_price = product_inventory.sale_price
                # origin quantity
                origin_quantity = order_item.quantity
                origin_spending = origin_quantity * sale_price
                # get quantity from form
                form_quantity = request.POST.get('quantity')
                # get updated spending
                new_spending = int(form_quantity) * sale_price
                # get the order
                order = order_item.order
                # get order total paid
                order_total_paid = order.total_paid
                new_total = order_total_paid - origin_spending + new_spending
                # update order total paid
                order.total_paid = new_total
                order.save()
                form = OrderItemForm(request.POST, instance=order_item)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(
                        '/orders/order_details/{}'.format(order_item.order.id)
                    )
                context = {
                    'form': form,
                    'order_item': order_item,
                }
                return render(request, 'orders/edit_order_item.html', context)
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


class DeleteOrderItemView(View):
    """View to delete order item"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.role.id == 3:
                order_item = get_object_or_404(
                    OrderItem,
                    id=kwargs['order_item_id']
                )
                context = {
                    'order_item': order_item,
                }
                return render(
                    request,
                    'orders/delete_order_item.html',
                    context
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
        if request.user.is_authenticated:
            if request.user.profile.role.id == 3:
                order_item = get_object_or_404(
                    OrderItem,
                    id=kwargs['order_item_id']
                )
                product_inventory = get_object_or_404(
                    ProductInventory,
                    id=order_item.product_inventory.id
                )
                # get sale_price
                sale_price = product_inventory.sale_price
                # origin quantity
                origin_quantity = order_item.quantity
                origin_spending = origin_quantity * sale_price
                # get the order
                order = order_item.order
                # get order total paid
                order_total_paid = order.total_paid
                new_total = order_total_paid - origin_spending
                # update order total paid
                order.total_paid = new_total
                order.save()
                order_item.delete()
                return HttpResponseRedirect(
                    '/orders/order_details/{}'.format(order.id)
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


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)
    # send email to the customer
    order = Order.objects.get(order_key=data)
    # get this order
    order_id = order.id
    order_obj = Order.objects.get(id=order_id)
    customer = order_obj.user
    subject = 'Payment Confirmation'
    # get the order total paid
    order_total_paid = order_obj.total_paid
    order_num = str(order_obj.order_number)
    link = (
        'https://wowder.herokuapp.com/orders/' + str(customer.username) +
        '/my_orders/' + order_num + '/'
    )
    subject, from_email, to = (
        'Payment Confirmation', 'wow@der.com', str(customer.email)
    )
    text_content = ''
    html_content = '<h1>Payment Confirmation</h2>' \
        '<p>Your payment of $' + str(order_total_paid) \
        + ' has been confirmed.</p>' \
        '<p>You can view your order details by ' \
        'clicking on your order information link below:</p>' \
        '<strong>Order ID: </strong>' \
        '<a href=' + link + '>' + order_num + \
        '</a><br><p>Thank you for shopping with us!</p>' \
        '<em>WoWder shop</em>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


class UserOrdersView(View):
    """View for user orders page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            p = Paginator(Order.objects.filter(user=user).filter(
                billing_status=True
            ), 15)
            page = request.GET.get('page')
            orders = p.get_page(page)
            return render(
                request, 'orders/user_orders.html', {'orders': orders}
            )
        else:
            return render(
                request, 'account/login.html',
            )


class UserOrderDetailsView(View):
    """View for user order details page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order = get_object_or_404(
                Order,
                order_number=kwargs['order_number']
            )
            # get order items
            order_items = OrderItem.objects.filter(order=order)
            all_items = Order.get_order_items(order)
            # check if the order is completed
            user_reviews_for_this_order = Review.objects.filter(
                order=order,
                user=request.user
            )
            # get which products are in these reviews
            products_in_reviews = []
            for review in user_reviews_for_this_order:
                products_in_reviews.append(review.product)
            context = {
                'order': order,
                'order_items': order_items,
                'all_items': all_items,
                'products_in_reviews': products_in_reviews,
            }
            if order.user == request.user:
                return render(
                    request,
                    'orders/user_order_details.html',
                    context,
                )
            else:
                return render(
                    request, 'profiles/access_denied.html',
                )
        else:
            return render(
                request, 'account/login.html',
            )
