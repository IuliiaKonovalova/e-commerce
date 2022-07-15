"""Views for orders app."""
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator

from reviews.models import Review
from .models import Order, OrderItem
from bag.contexts import bag_contents


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
                p = Paginator(Order.objects.filter(user=request.user), 25)
                page = request.GET.get('page')
                orders = p.get_page(page)
                context = {
                    'orders': orders,
                }
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
                    print(request.POST)
                    order_id =  request.POST.get('order_id')
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
                print(request.POST)
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
                total_paid = str(bag['total'])
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
                    print(order)
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


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


class UserOrdersView(View):
    """View for user orders page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            p = Paginator(Order.objects.filter(user=user).filter(
                billing_status=True
            ), 25)
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
            order = get_object_or_404(Order, id=kwargs['order_id'])
            # get order items
            order_items = OrderItem.objects.filter(order=order)
            print(order_items)
            all_items = Order.get_order_items(order)
            print(all_items)
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