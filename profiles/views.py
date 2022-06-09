"""Views for the profiles app."""
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Role, Profile, Address


class UserProfileView(View):
    """View for the profile page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            my_profile = get_object_or_404(
                Profile,
                user=request.user
            )
            my_addresses = Address.objects.filter(
                user=request.user
            )
            context = {
                'my_profile': my_profile,
                'my_addresses': my_addresses
            }
            return render(
                request,
                'profiles/my_profile.html',
                context
            )
        else:
            return render(
                request,
                'account/login.html'
            )