"""Views for the promotions app."""
from django.views import View
from django.shortcuts import render
from .models import Promotion
from inventory.models import ProductInventory


class PromotionsListView(View):
    """View for the promotions list page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(request.user.profile.role, 'is authenticated')
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                promotions = Promotion.objects.all()
                context = {
                    'promotions': promotions,
                }
                return render(
                    request,
                    'promotions/promotions_list.html',
                    context
                )
        else:
            return render(
                request,
                'account/login.html',
            )
