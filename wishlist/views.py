"""Views for the wishlist app."""
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Wishlist
from inventory.models import Product


class WishlistDisplayView(View):
    """View for the wishlist display page."""
    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.get(user=request.user)
            # get products in the wishlist
            products = wishlist.products.all()
            context = {
                'products': products,
            }
            return render(
                request,
                'wishlist/wishlist_display.html',
                context
            )
        else:
            return render(
                request,
                'account/login.html'
            )

