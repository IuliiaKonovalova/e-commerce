"""ecommerce_project URL Configuration"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('profiles/', include('profiles.urls')),
    path('inventory/', include('inventory.urls')),
    path('bag/', include('bag.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('promotions/', include('promotions.urls')),
]
