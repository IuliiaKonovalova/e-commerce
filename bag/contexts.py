"""Context for the shopping bag."""
from decimal import Decimal
from django.shortcuts import get_object_or_404
from inventory.models import ProductInventory
from promotions.models import Promotion


def bag_contents(request):
    """Return the contents of the shopping bag."""
    bag_items = []
    total = 0
    product_count = 0
    product_item_total = 0
    promo_price = 0
    bag = request.session.get('bag', {})
    if bag:
        for item_id, item_data in bag.items():
            if isinstance(item_data, int):
                product_count += item_data
                product_inventory = get_object_or_404(
                    ProductInventory, id=item_id
                )
                units = product_inventory.stock.units
                product_item_total = product_inventory.sale_price * item_data
                total += product_inventory.sale_price * item_data
                bag_items.append({
                    'product_inventory': product_inventory,
                    'product_item_total': product_item_total,
                    'quantity': item_data,
                    'units': units,
                })
    total_promo = request.session.get('total_promo', {})
    if total_promo:
        total_promo = float(total_promo)
        promo_decimal = round(
                            Decimal(total_promo), 2
                        )
        total_promo = promo_decimal
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'product_item_total': product_item_total,
        'promo_price': total_promo,
    }
    return context
