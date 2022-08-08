from django.views import View
from django.shortcuts import render


class HomeView(View):
    """View for the home page."""
    def get(self, request):
        """Return the home page."""
        return render(request, 'home/home.html')
