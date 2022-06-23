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
            return JsonResponse(
                {
                    'success': True,
                    'quantity': quantity,
                    'product_item_total': product_item_total,
                    'message_alert': message_alert,
                }
            )
        return JsonResponse({'success': False})


class AddUnitToBagAJAXView(View):
    """View for the add unit to bag AJAX."""
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            print('AJAX request')
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
            # get bag_items from the context
            print(bag, 'this is a bag')
            print(product_inventory_id, 'this is a product_inventory_id')
            # get quantity from the bag for this product_inventory_id
            quantity = bag.get(product_inventory_id, 0)
            # check type of quantity
            print(type(quantity), 'this is a type of quantity')
            print(quantity, 'this is a quantity')
            # get sale_price from the product_inventory
            sale_price = product_inventory.sale_price
            print(sale_price, 'this is a sale_price')
            # get product_item_total from
            product_item_total = sale_price * quantity
            print(product_item_total, 'this is a product_item_total')
            # save the bag to the session
            request.session['bag'] = bag
            return JsonResponse(
                {
                    'success': True,
                    'quantity': quantity,
                    'product_item_total': product_item_total,
                    'message_alert': message_alert,
                }
            )
        return JsonResponse({'success': False})

