"""Views for the bag app."""
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from inventory.models import ProductInventory


class BagDisplayView(View):
    """View for the bag display page."""
    def get(self, request, *args, **kwargs):
        return render(request, 'bag/bag_display.html')


class AddToBagAJAXView(View):
    """View for the add to bag AJAX."""
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            print('AJAX request')
            product_inventory_id = request.POST.get('product_inventory_id')
            quantity = request.POST.get('quantity')
            product_inventory = get_object_or_404(
                ProductInventory, id=product_inventory_id
            )
            bag = request.session.get('bag', {})
            message_alert = ''
            if product_inventory_id in bag:
                bag[product_inventory_id] += int(quantity)
                message_alert = f'{product_inventory.product.name} UPDATED.'
            else:
                bag[product_inventory_id] = int(quantity)
                message_alert = (
                    f'{product_inventory.product.name} ADDED TO BAG.'
                )
            request.session['bag'] = bag
            return JsonResponse(
                {
                    'success': True,
                    'message_alert': message_alert,
                }
            )
        return JsonResponse({'success': False})

