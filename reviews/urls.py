"""URLs for the reviews app."""
from django.urls import path
from .views import (
    AddReviewView,
)


urlpatterns = [
    path('add_review/<int:order_id>/<int:product>/',
    AddReviewView.as_view(), name='add_review'),
]