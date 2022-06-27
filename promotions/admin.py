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

    def get_readonly_fields(self, request, obj=None):
        """Set readonly fields."""
        if obj:
            return self.readonly_fields + ('created_at', 'updated_at')
        return self.readonly_fields

    def get_fieldsets(self, request, obj=None):
        """Set fieldsets."""
        if obj:
            return self.fieldsets + (
                ('Readonly fields', {'fields': ('created_at', 'updated_at')}),
            )
        return self.fieldsets

    def get_list_display(self, request):
        """Set list display."""
        return self.list_display + ('created_at', 'updated_at')

    def get_list_filter(self, request):
        """Set list filter."""
        return self.list_filter + ('created_at', 'updated_at')

    def get_search_fields(self, request):
        """Set search fields."""
        return self.search_fields + ('created_at', 'updated_at')
