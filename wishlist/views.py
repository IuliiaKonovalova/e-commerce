"""Views for the wishlist app."""
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Wishlist
from inventory.models import Product


class WishlistDisplayView(View):
    """View for the wishlist display page."""
    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.get(user=request.user)
            # get products in the wishlist
            p = Paginator(wishlist.products.all(), 21)
            page = request.GET.get('page')
            products = p.get_page(page)
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


class AddRemoveProductWishlistAJAXView(View):
    """View for the add to wishlist AJAX."""
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.is_ajax():
                product_id = request.POST.get('product_id')
                product = get_object_or_404(Product, id=product_id)
                wishlist = Wishlist.objects.get(user=request.user)
                message_alert = ''
                product_in_wishlist = False
                if wishlist.add_to_wishlist(product):
                    product_in_wishlist = True
                    message_alert = (
                        f'{product.name} added to wishlist.'
                    )
                else:
                    wishlist.remove_from_wishlist(product)
                    product_in_wishlist = False
                    message_alert = (
                        f'{product.name} removed from wishlist.'
                    )
                return JsonResponse(
                    {
                        'success': True,
                        'product_in_wishlist': product_in_wishlist,
                        'message_alert': message_alert,
                    }
                )
            else:
                return JsonResponse(
                    {
                        'success': False,
                        'message_alert': 'Not a valid request.',
                    }
                )
        else:
            message_alert = 'You must be logged in to add to wishlist.'
            return JsonResponse(
                {
                    'success': False,
                    'message_alert': message_alert,
                }
            )


class EmptyWishlistAJAXView(View):
    """View for the empty wishlist AJAX."""
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.is_ajax():
                wishlist = Wishlist.objects.get(user=request.user)
                wishlist.remove_all_from_wishlist()
                return JsonResponse(
                    {
                        'success': True,
                        'message_alert': 'Wishlist is now empty.',
                    }
                )
            else:
                return JsonResponse(
                    {
                        'success': False,
                        'message_alert': 'Something went wrong.',
                    }
                )
        else:
            message_alert = 'You must be logged in to empty wishlist.'
            return JsonResponse(
                {
                    'success': False,
                    'message_alert': message_alert,
                }
            )
