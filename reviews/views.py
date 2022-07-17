"""Views for reviews app."""
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from orders.models import Order
from reviews.models import Review, ReviewImage
from inventory.models import Product


class ReviewDetailView(View):
    """View for review detail."""
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        # get review
        review = get_object_or_404(
            Review,
            order=order,
            product=product,
        )
        images = ReviewImage.objects.filter(review=review)
        context = {
            'product': product,
            'review': review,
            'images': images,
        }
        return render(request, 'reviews/review_detail.html', context)


class AddReviewView(View):
    """View for add review page."""

    def get(self, request, *args, **kwargs):
        """Get method for add review page."""
        if request.user.is_authenticated:
            # check if the order.user is request.user
            order_id = kwargs['order_id']
            order = get_object_or_404(Order, id=order_id)
            if order.user == request.user:
                product_id = kwargs['product_id']
                product = get_object_or_404(Product, id=product_id)
                user = request.user
                # check if this user has already reviewed this product
                if Review.objects.filter(
                    user=user,
                    product=product,
                    order=order,
                ).exists():
                    return render(
                        request,
                        'reviews/review_already_exists.html',
                        {'product': product, 'order': order}
                    )
                else:
                    context = {
                        'order': order,
                        'product': product,
                        'user': user,
                    }
                    return render(request, 'reviews/add_review.html', context)
            else:
                return render(
                    request,
                    'profiles/access_denied.html',
                )
        else:
            return render(
                request,
                'account/login.html',
            )


