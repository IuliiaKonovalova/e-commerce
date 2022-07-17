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


class AddReviewWithImagesAJAXView(View):
    """View for add review with images AJAX."""

    def post(self, request, *args, **kwargs):
        """Post method for add review with images AJAX."""
        if request.user.is_authenticated:
            if request.is_ajax():
                order_id = request.POST.get('order_id')
                print('order_id', order_id)
                order = get_object_or_404(Order, id=order_id)
                print('order', order)
                product_id = request.POST.get('product_id')
                print('product_id', product_id)
                product = get_object_or_404(Product, id=product_id)
                print('product', product)
                user = request.user
                print('user', user)
                comment = request.POST.get('comment')
                print('comment', comment)
                rating = request.POST.get('rating')
                print('rating', rating)
                if Review.objects.filter(
                    user=user,
                    product=product,
                    order=order,
                ).exists():
                    review_id = Review.objects.get(
                        user=user,
                        product=product,
                        order=order,
                    ).id
                    return JsonResponse(
                        {'success': False, 'review_id': review_id}
                    )
                else:
                    review = Review.objects.create(
                        order=order,
                        product=product,
                        user=user,
                        comment=comment,
                        rating=rating,
                    )
                    print('review', review)
                    images = request.FILES.getlist('images')
                    print('images', images)
                    for image in request.FILES.getlist('images'):
                        ReviewImage.objects.create(
                            review=review,
                            image=image,
                        )
                    return JsonResponse(
                        {'success': True, 'review_id': review.id}
                    )
            else:
                return JsonResponse({'success': False})
