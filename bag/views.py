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

