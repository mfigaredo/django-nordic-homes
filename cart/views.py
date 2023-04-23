from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from product.models import Product

from .cart import Cart

# Create your views here.
def add_to_cart(request, product_id):
  cart = Cart(request)
  cart.add(product_id)

  return render(request, 'cart/partials/menu_cart.html', {})

def cart(request):
  print(Cart(request))
  return render(request, 'cart/cart.html')

def success(request):
  return render(request, 'cart/success.html')

def update_cart(request, product_id, action):
  cart = Cart(request)
  if action == 'increment':
    cart.add(product_id, 1, True)
  else:
    cart.add(product_id, -1, True)
  
  product = Product.objects.get(pk=product_id)

  if cart.get_item(product_id):
    quantity = cart.get_item(product_id)['quantity']

    item = {
      'product': {
        'id': product.id,
        'name': product.name,
        'image': product.image,
        'get_thumbnail': product.get_thumbnail(),
        'price': product.price / 100.00,
      },
      'total_price': (quantity * product.price) / 100.00,
      'quantity': quantity,
    }
  else:
    item = None

  response = render(request, 'cart/partials/cart_item.html', {'item': item, 'cart_len': len(cart), })
  response['HX-Trigger'] = 'update-menu-cart'
  return response

@login_required
def checkout(request):
  cart = Cart(request)
  if len(cart) == 0:
    return redirect('cart')
  pub_key = settings.STRIPE_API_KEY_PUBLISHABLE
  return render(request, 'cart/checkout.html', {'pub_key': pub_key, })

def empty_cart(request):
  cart = Cart(request)
  cart.remove('*')
  return HttpResponse('Cart is now emptied')

def hx_menu_cart(request):
  return render(request, 'cart/partials/menu_cart.html')

def hx_cart_total(request):
  return render(request, 'cart/partials/cart_total.html', {})