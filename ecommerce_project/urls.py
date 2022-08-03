"""ecommerce_project URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from .views import handler404, handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('profiles/', include('profiles.urls')),
    path('inventory/', include('inventory.urls')),
    path('bag/', include('bag.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('promotions/', include('promotions.urls')),
    path('email_notifications/', include('email_notifications.urls')),
    path('personnel/', include('personnel.urls')),
    path('payment/', include('payment.urls')),
    path('orders/', include('orders.urls')),
    path('reviews/', include('reviews.urls')),
]

handler404 = 'ecommerce_project.views.handler404'
handler500 = 'ecommerce_project.views.handler500'
