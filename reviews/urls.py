"""URLs for the reviews app."""
from django.urls import path
from .views import (
    ReviewDetailView,
    AddReviewView,
    AddReviewWithImagesAJAXView,
)


urlpatterns = [
    path(
        'review/<int:order_id>/<int:product_id>/',
        ReviewDetailView.as_view(),
        name='review',
    ),
    path(
        'add_review/<int:order_id>/<int:product_id>/',
        AddReviewView.as_view(),
        name='add_review'
    ),
    path(
        'add_review_with_images_ajax/',
        AddReviewWithImagesAJAXView.as_view(),
        name='add_review_with_images_ajax'
    ),
]