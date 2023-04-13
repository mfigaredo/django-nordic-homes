from django.conf import settings
from product.models import Product


class Cart(object):

  def __init__(self, request):
    self.session = request.session
    cart = self.session.get(settings.CART_SESSION_ID)

    if not cart:
      cart = self.session[settings.CART_SESSION_ID] = {}

    self.cart = cart

  def __iter__(self):

    products = Product.objects.filter(id__in=self.cart.keys())

    for p in self.cart.keys():
      self.cart[str(p)]['product'] = products.get(pk=p)
    
    for item in self.cart.values():
      # item['total_price'] = item['product'].price * item['quantity']

      yield item

  def __len__(self):
    return sum(item['quantity'] for item in self.cart.values() ) or 0
  
  def save(self):

    products = Product.objects.filter(id__in=self.cart.keys())
    for item in self.cart.values():
        product = products.get(pk=item['id'])
        self.cart[str(product.id)]['price'] = product.price / 100.00
        self.cart[str(product.id)]['total_price'] = product.price * item['quantity'] / 100.00

    self.session[settings.CART_SESSION_ID] = self.cart
    self.session.modified = True
  
  def add(self, product_id, quantity=1, update_quantity=False):
    product_id = str(product_id)

    if product_id not in self.cart:
      # product = Product.objects.get(pk=product_id)
      self.cart[product_id] = {'quantity': quantity, 'id': product_id, 'price': -1, 'total_price': -1, }

    if update_quantity:
      self.cart[product_id]['quantity'] += int(quantity)
      # self.cart[product_id]['total_price'] = self.cart[product_id]['quantity'] * self.cart[product_id]['price']

      if self.cart[product_id]['quantity'] == 0:
        # self.cart.remove(product_id)
        # pass
        print(self.cart[product_id])
        del self.cart[product_id]
    
    self.save()
    
  def remove(self, product_id):
    product_id = str(product_id)

    if product_id in self.cart:
      del self.cart[product_id]
      self.save()

    if product_id == '*':
      self.cart = {}
      self.save()
      print('empty cart')

  def clear(self):
    del self.session[settings.CART_SESSION_ID]
    self.session.modified = True

  def get_total_cost(self):
    return sum(item['total_price'] for item in self.cart.values() )/1
  
  # def display_total_cost(self):
  #   return (self.get_total_cost())
  
  def get_item(self, product_id):
    if str(product_id) in self.cart:
      return self.cart[str(product_id)]
    return None

  def __str__(self):
    return str(dict(self.cart))