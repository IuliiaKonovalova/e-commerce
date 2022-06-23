from django.shortcuts import get_object_or_404
from inventory.models import ProductInventory


def bag_contents(request):
    """Return the contents of the shopping bag."""
    bag_items = []
    total = 0
    product_count = 0
    product_item_total = 0
    bag = request.session.get('bag', {})
    if bag:
      for item_id, item_data in bag.items():
          if isinstance(item_data, int):
              product_count += item_data
              product_inventory = get_object_or_404(
                  ProductInventory, id=item_id
              )
              units = product_inventory.stock.units
              print(units)
              print(product_count)
              if units < product_count:
                  product_count = units
              product_item_total = product_inventory.sale_price * item_data
              total += product_inventory.sale_price * item_data
              
              bag_items.append({
                  'product_inventory': product_inventory,
                  'product_item_total': product_item_total,
                  'quantity': item_data,
                  'units': units,
              })
    print(bag_items)
    print(total)
    print(product_count)
    print(product_item_total)



    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'product_item_total': product_item_total,
    }
    return context