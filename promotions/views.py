"""Views for the promotions app."""
from django.views import View
from django.shortcuts import render,redirect
from .models import Promotion
from inventory.models import ProductInventory
from .forms import PromotionForm


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


class AddPromotionView(View):
    """View for the add promotion page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(request.user.profile.role, 'is authenticated')
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                form = PromotionForm(request.POST)
                return render(
                    request,
                    'promotions/add_promotion.html',
                    {'form': form}
                )
        else:
            return render(
                request,
                'account/login.html',
            )

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(request.user.profile.role, 'is authenticated')
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                form = PromotionForm(request.POST)
                if form.is_valid():
                    promotion = form.save(commit=False)
                    print(form)
                    print('products_inventory_in_promotion')
                    products_inventory_in_promotion = form.cleaned_data[
                        'products_inventory_in_promotion'
                    ]
                    print(products_inventory_in_promotion)
                    promotion.save()
                    promotion.products_inventory_in_promotion.set(
                        products_inventory_in_promotion
                    )
                    promotion.save()
                      
                    return redirect('promotions_list')
                else:
                    return render(
                        request,
                        'promotions/add_promotion.html',
                        {'form': form}
                    )


class EditPromotionView(View):
    """View for the edit promotion page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(request.user.profile.role, 'is authenticated')
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                promotion = Promotion.objects.get(id=kwargs['pk'])
                form = PromotionForm(instance=promotion)
                return render(
                    request,
                    'promotions/edit_promotion.html',
                    {'form': form, 'promotion': promotion}
                )
        else:
            return render(
                request,
                'account/login.html',
            )

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(request.user.profile.role, 'is authenticated')
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                promotion = Promotion.objects.get(id=kwargs['pk'])
                form = PromotionForm(request.POST, instance=promotion)
                if form.is_valid():
                    promotion = form.save(commit=False)
                    print(form)
                    print('products_inventory_in_promotion')
                    products_inventory_in_promotion = form.cleaned_data[
                        'products_inventory_in_promotion'
                    ]
                    print(products_inventory_in_promotion)
                    promotion.save()
                    promotion.products_inventory_in_promotion.set(
                        products_inventory_in_promotion
                    )
                    promotion.save()
                      
                    return redirect('promotions_list')
                else:
                    return render(
                        request,
                        'promotions/edit_promotion.html',
                        {'form': form, 'promotion': promotion}
                )
