"""Views for payment app."""
import json

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from profiles.models import Role, Profile, Address
from django.views.generic.base import TemplateView

from bag.contexts import bag_contents



@login_required
def BasketView(request):
    """View for payment page."""
    my_profile = get_object_or_404(
        Profile,
        user=request.user
    )
    primary_address = Address.objects.get(
        user=request.user,
        is_primary=True
    )
    print(primary_address.city)
    bag = bag_contents(request)
    print(bag)
    # get total out of bag dict
    total_sum = str(bag['total'])
    print(total_sum)
    total = total_sum.replace('.', '')
    total = int(total)
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe.api_key = settings.STRIPE_SECRET_KEY
    print(stripe_public_key)
    # ''
    intent = stripe.PaymentIntent.create(
        print('TOTAL', total),
        amount=total,
        currency='usd',
        metadata={'userid': request.user.id}
    )
    context = {
        'my_profile': my_profile,
        'primary_address': primary_address,
        'total_sum': total_sum,
        'client_secret': intent.client_secret,
        'stripe_public_key': stripe_public_key,
    }
    return render(request, 'payment/payment.html', context)


def order_placed(request):
    """View for order placed page."""
    bag = bag_contents(request)
    bag_items = bag['bag_items']
    print(bag_items)
    for item in bag_items:
        sold_product_inventory = item['product_inventory']
        sold_quantity = item['quantity']
        sold_product_inventory.stock.units_sold += sold_quantity
        sold_product_inventory.stock.units -= sold_quantity
        sold_product_inventory.stock.save()
    # clear the bag
    bag = request.session.get('bag', {})
    bag.clear()
    request.session['bag'] = bag
    return render(request, 'payment/order_placed.html')
