"""Admin for the profile app."""
from django.contrib import admin
from .models import Role, Profile, Address


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin for the Role model."""
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin for the Profile model."""
    list_display = (
        'user',
        'first_name',
        'last_name',
        'birthday',
        'avatar',
        'subscription'
    )
    list_filter = (
        'user',
        'first_name',
        'last_name',
        'birthday',
        'avatar',
        'subscription'
    )
    search_fields = (
        'user',
        'first_name',
        'last_name',
        'birthday',
        'avatar',
        'subscription'
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin for the Address model."""
    list_display = (
        'country',
        'county_region',
        'city',
        'address_line',
        'zip_code',
        'phone_number',
        'is_primary'
    )
    list_filter = (
        'country',
        'county_region',
        'city',
        'address_line',
        'zip_code',
        'phone_number',
        'is_primary'
    )
    search_fields = (
        'country',
        'county_region',
        'city',
        'address_line',
        'zip_code',
        'phone_number',
        'is_primary'
    )
