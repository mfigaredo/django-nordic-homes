from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review

# Create your views here.
def product(request, slug):
  # product = Product.objects.get(slug=slug)
  product = get_object_or_404(Product, slug=slug)

  if request.method == 'POST':
    rating = request.POST.get('rating', 3)
    content = request.POST.get('content', '')

    if content:
      reviews = Review.objects.filter(created_by=request.user, product=product)

      if reviews.count() > 0:
        review = reviews.first()
        review.rating = rating
        review.content = content
        review.save()
      else:
        review = Review.objects.create(
          rating=rating, 
          content=content, 
          created_by=request.user,
          product=product,
        )
      return redirect('product', slug=slug)

  return render(request, 'product/product.html', {'product': product, })
