"""Views for payment app."""
from decimal import Decimal
import json

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from profiles.models import Profile, Address
from django.views.generic.base import TemplateView
from bag.contexts import bag_contents
from orders.views import payment_confirmation
from promotions.models import Promotion


@login_required
def BasketView(request):
    """View for payment page."""
    my_profile = get_object_or_404(
        Profile,
        user=request.user
    )
    bag = bag_contents(request)
    # get total out of bag dict
    promo_price = bag['promo_price']
    if promo_price and promo_price != 0:
        total_final = promo_price
    else:
        total_final = bag['total']
    total_sum = str(total_final)
    total = total_sum.replace('.', '')
    total = int(total)
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='usd',
        metadata={'userid': request.user.id}
    )
    # check if user has addresses
    if request.user.addresses.count() == 0:
        pass
    else:
        # check if there is a primary address
        if request.user.addresses.filter(is_primary=True).exists():
            primary_address = Address.objects.get(
                user=request.user,
                is_primary=True
            )
            context = {
                'my_profile': my_profile,
                'primary_address': primary_address,
                'total_sum': total_sum,
                'client_secret': intent.client_secret,
                'stripe_public_key': stripe_public_key,
            }
            return render(request, 'payment/payment.html', context)
    context = {
        'my_profile': my_profile,
        'total_sum': total_sum,
        'client_secret': intent.client_secret,
        'stripe_public_key': stripe_public_key,
    }
    return render(request, 'payment/payment.html', context)


def order_placed(request):
    """View for order placed page."""
    bag = bag_contents(request)
    bag_items = bag['bag_items']
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


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return HttpResponse(status=400)
    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)
    else:
        print('Unhandled event type {}'.format(event.type))
    return HttpResponse(status=200)
