"""Views for the bag app."""
from decimal import Decimal
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from inventory.models import ProductInventory
from promotions.models import Promotion
from .contexts import bag_contents


class BagDisplayView(View):
    """View for the bag display page."""
    def get(self, request, *args, **kwargs):
        # UPDATE TOTAL PROMO
        request.session['total_promo'] = 0
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
                # UPDATE TOTAL PROMO
                request.session['total_promo'] = 0
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
                    # UPDATE TOTAL PROMO
                    request.session['total_promo'] = 0
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
                    # UPDATE TOTAL PROMO
                    request.session['total_promo'] = 0
            request.session['bag'] = bag
            contents = bag_contents(request)
            total = contents['total']
            product_count = contents['product_count']
            request.session['bag'] = bag
            return JsonResponse(
                {
                    'success': True,
                    'message_alert': message_alert,
                    'total': total,
                    'product_count': product_count,
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
                # UPDATE TOTAL PROMO
                request.session['total_promo'] = 0
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


class PromoCodeAJAXView(View):
    """View for the promo code AJAX."""
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            promo_code = request.POST.get('promo_code')
            promo = get_object_or_404(
                Promotion,
                promotion_code=promo_code
            )
            if promo.active and promo.is_active_now():
                bag = request.session.get('bag', {})
                # get total from the bag
                total = bag_contents(request)['total']
                total_promo = total
                # get bag_items
                bag_items = bag.items()
                promo_items = promo.get_products_in_promotion()
                for item in bag_items:
                    # get product_inventory
                    product_inventory = get_object_or_404(
                        ProductInventory,
                        id=item[0]
                    )
                    # check if the product is in the promo
                    if product_inventory in promo_items:
                        reduction = promo.promotion_reduction
                        reduction_percent = float(reduction) * 0.01
                        price = product_inventory.sale_price
                        price_after_reduction = (
                            float(price) * reduction_percent
                        ) * item[1]
                        price_after_reduction = round(
                            Decimal(price_after_reduction), 2
                        )
                        total_promo -= price_after_reduction
                        request.session['total_promo'] = str(total_promo)
                        bag_contents(request)['total_promo'] = str(total_promo)
                request.session['bag'] = bag
                return JsonResponse(
                    {
                        'success': True,
                        'total_promo': total_promo,
                    }
                )
            else:
                alert_message = 'Promo code is not active.'
                return JsonResponse(
                    {
                        'success': False,
                        'alert_message': alert_message
                    }
                )
        alert_message = 'Something went wrong. Please try again.'
        return JsonResponse(
            {
                'success': False,
                'alert_message': alert_message
            }
        )


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
                # UPDATE TOTAL PROMO
                request.session['total_promo'] = 0
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
                # UPDATE TOTAL PROMO
                request.session['total_promo'] = 0
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
            # UPDATE TOTAL PROMO
            request.session['total_promo'] = 0
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
