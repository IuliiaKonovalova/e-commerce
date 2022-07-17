"""Admin for reviews app."""
from django.contrib import admin
from .models import Review, ReviewImage


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin for the Review model."""
    list_display = (
        'user',
        'product',
        'rating',
        'comment',
    )
    list_filter = ('user', 'product', 'rating', 'comment')
    search_fields = ('user', 'product', 'rating', 'comment')


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    """Admin for the ReviewImage model."""
    list_display = ('review', 'image')
    list_filter = ('review', 'image')
    search_fields = ('review', 'image')
