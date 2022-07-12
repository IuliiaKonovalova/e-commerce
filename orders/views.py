"""Views for orders app."""
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
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
                orders = Order.objects.filter(user=request.user)
                context = {
                    'orders': orders,
                }
                return render(request, 'orders/orders.html', context)
        else:
            return render(
                request,
                'account/login.html',
            )
