"""Views for the bag app."""
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from inventory.models import ProductInventory
from .contexts import bag_contents



class BagDisplayView(View):
    """View for the bag display page."""
    def get(self, request, *args, **kwargs):
        return render(request, 'bag/bag_display.html')


class AddToBagAJAXView(View):
    """View for the add to bag AJAX."""
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            product_inventory_id = request.POST.get('product_inventory_id')
            quantity = request.POST.get('quantity')
            product_inventory = get_object_or_404(
                ProductInventory, id=product_inventory_id
            )
            bag = request.session.get('bag', {})
            message_alert = ''
            units = product_inventory.stock.units
            if product_inventory_id in bag:
                request.session['bag'] = bag
                bag = request.session.get('bag', {})
                quantity_in_bag = bag.get(product_inventory_id, 0)
                appropriate_quantity = int(quantity) + quantity_in_bag
                if appropriate_quantity > units:
                    quantity = units
                    bag[product_inventory_id] = int(quantity)
                    quantity_to_add = int(quantity) - quantity_in_bag
                    message_alert = (
                        'Not enough units in stock.'
                        f' Only {quantity_to_add} added.'
                    )
                else:
                    bag[product_inventory_id] += int(quantity)
                    message_alert = (
                        f'{product_inventory.product.name} UPDATED.'
                    )
            else:
                if units < int(quantity):
                    quantity = units
                    message_alert = (
                        f'Not enough units in stock. Only {units} added.'
                    )
                    bag[product_inventory_id] = int(quantity)
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


class RemoveUnitFromBagAJAXView(View):
    """View for the remove from bag AJAX."""
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            product_inventory_id = request.POST.get('product_inventory_id')
            product_inventory = get_object_or_404(
                ProductInventory, id=product_inventory_id
            )
            bag = request.session.get('bag', {})
            message_alert = ''
            if product_inventory_id in bag:
                if bag[product_inventory_id] > 1:
                    bag[product_inventory_id] -= 1
                    message_alert = (
                        f'{product_inventory.product.name} UPDATED.'
                    )
                    
                else:
                    bag.pop(product_inventory_id)
                    message_alert = (
                        f'{product_inventory.product.name} REMOVED.'
                    )
            request.session['bag'] = bag
            bag = request.session.get('bag', {})
            # get quantity from the bag for this product_inventory_id
            quantity = bag.get(product_inventory_id, 0)
            # get sale_price from the product_inventory
            sale_price = product_inventory.sale_price
            # get product_item_total from
            product_item_total = sale_price * quantity
            request.session['bag'] = bag
            contents = bag_contents(request)
            total = contents['total']
            product_count = contents['product_count']
            request.session['bag'] = bag
            return JsonResponse(
                {
                    'success': True,
                    'quantity': quantity,
                    'product_item_total': product_item_total,
                    'message_alert': message_alert,
                    'total': total,
                    'product_count': product_count,
                }
            )
        return JsonResponse({'success': False})


class AddUnitToBagAJAXView(View):
    """View for the add unit to bag AJAX."""
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            product_inventory_id = request.POST.get('product_inventory_id')
            product_inventory = get_object_or_404(
                ProductInventory, id=product_inventory_id
            )
            bag = request.session.get('bag', {})
            message_alert = ''
            if product_inventory_id in bag:
                bag[product_inventory_id] += 1
                message_alert = f'{product_inventory.product.name} UPDATED.'
            else:
                message_alert = 'This product was not in the bag.'
            bag = request.session.get('bag', {})
            # get quantity from the bag for this product_inventory_id
            quantity = bag.get(product_inventory_id, 0)
            # get sale_price from the product_inventory
            sale_price = product_inventory.sale_price
            # get product_item_total from
            product_item_total = sale_price * quantity
            request.session['bag'] = bag
            contents = bag_contents(request)
            total = contents['total']
            product_count = contents['product_count']
            return JsonResponse(
                {
                    'success': True,
                    'quantity': quantity,
                    'product_item_total': product_item_total,
                    'message_alert': message_alert,
                    'total': total,
                    'product_count': product_count,
                }
            )
        return JsonResponse({'success': False})


class RemoveAllItemUnitsFromBagAJAXView(View):
    """View for the remove all item units from bag AJAX."""
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            product_inventory_id = request.POST.get('product_inventory_id')
            product_inventory = get_object_or_404(
                ProductInventory, id=product_inventory_id
            )
            bag = request.session.get('bag', {})
            message_alert = ''
            if product_inventory_id in bag:
                bag.pop(product_inventory_id)
                message_alert = (
                    f'{product_inventory.product.name} REMOVED.'
                )
            request.session['bag'] = bag
            bag = request.session.get('bag', {})
            request.session['bag'] = bag
            contents = bag_contents(request)
            total = contents['total']
            product_count = contents['product_count']
            return JsonResponse(
                {
                    'success': True,
                    'message_alert': message_alert,
                    'total': total,
                    'product_count': product_count,
                }
            )
        return JsonResponse({'success': False})


class RemoveAllBagAJAXView(View):
    """View for the remove all bag AJAX."""
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            bag = request.session.get('bag', {})
            bag.clear()
            request.session['bag'] = bag
            contents = bag_contents(request)
            total = contents['total']
            product_count = contents['product_count']
            message_alert = 'Bag is now empty.'
            return JsonResponse(
                {
                    'success': True,
                    'total': total,
                    'product_count': product_count,
                    'message_alert': message_alert,
                }
            )
        return JsonResponse({'success': False})
