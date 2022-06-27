"""Admin for the Promotions model."""
from django.contrib import admin
from .models import Promotion


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    """Admin for the Promotion model."""
    list_display = (
        'name',
        'description',
        'active',
        'promotion_code',
        'promotion_reduction',
        'start_date',
        'end_date',
    )
    prepopulated_fields = {'slug': ('name',)}
    list_filter = (
        'name',
        'description',
        'active',
        'promotion_code',
        'promotion_reduction',
    )
    search_fields = (
        'name',
        'description',
        'active',
        'promotion_code',
        'promotion_reduction',
    )
    ordering = ('-created_at',)
