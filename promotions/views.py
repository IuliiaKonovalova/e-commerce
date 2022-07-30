"""Views for the promotions app."""
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Promotion
from .forms import PromotionForm


class PromotionsListView(View):
    """View for the promotions list page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if user is a admin
            if request.user.profile.role.id == 1:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
            else:
                p = Paginator(Promotion.objects.all(), 10)
                page = request.GET.get('page')
                promotions = p.get_page(page)
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
            # Check if user is a admin
            if request.user.profile.role.id == 3:
                form = PromotionForm(request.POST)
                return render(
                    request,
                    'promotions/add_promotion.html',
                    {'form': form}
                )
            else:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
        else:
            return render(
                request,
                'account/login.html',
            )

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if user is a admin
            if request.user.profile.role.id == 3:
                form = PromotionForm(request.POST)
                if form.is_valid():
                    promotion = form.save(commit=False)
                    products_inventory_in_promotion = form.cleaned_data[
                        'products_inventory_in_promotion'
                    ]
                    promotion.save()
                    # Add the product inventories to the promotion
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
            else:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
        else:
            return render(
                request,
                'account/login.html',
            )


class EditPromotionView(View):
    """View for the edit promotion page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if user is a admin
            if request.user.profile.role.id == 3:
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
                    'profiles/access_denied.html',
                )
        else:
            return render(
                request,
                'account/login.html',
            )

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if user is a admin
            if request.user.profile.role.id == 3:
                promotion = Promotion.objects.get(id=kwargs['pk'])
                form = PromotionForm(request.POST, instance=promotion)
                if form.is_valid():
                    promotion = form.save(commit=False)
                    products_inventory_in_promotion = form.cleaned_data[
                        'products_inventory_in_promotion'
                    ]
                    promotion.save()
                    # Add set of product inventories to promotion
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
            else:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
        else:
            return render(
                request,
                'account/login.html',
            )


class DeletePromotionAJAXView(View):
    """View for the delete promotion AJAX."""
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if user is a admin
            if request.user.profile.role.id == 3:
                if request.is_ajax() and request.user.profile.role.id == 3:
                    promotion_id = request.POST.get('promotion_id')
                    promotion = Promotion.objects.get(id=promotion_id)
                    promotion.delete()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False})
            else:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
        else:
            return render(
                request,
                'account/login.html',
            )
