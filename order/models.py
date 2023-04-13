from django.db import models

from django.contrib.auth.models import User
from product.models import Product

# Create your models here.
class Order(models.Model):

  ORDERED = 'ordered'
  SHIPPED = 'shipped'

  STATUS_CHOICES = (
    (ORDERED, 'Ordered'),
    (SHIPPED, 'Shipped'),
  )

  user = models.ForeignKey(User, related_name='orders', blank=True, null=True, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  address = models.CharField(max_length=255)
  zipcode = models.CharField(max_length=20)
  place = models.CharField(max_length=255)
  phone = models.CharField(max_length=50)
  paid = models.BooleanField(default=False)
  paid_amount = models.IntegerField(blank=True, null=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def get_total_amount(self):
    # return sum([item['price'] for item in self.items.all().values('price')])/100.00
    if self.paid_amount:
      return self.paid_amount / 100.0
    return 0
  
  class Meta:
    ordering = ('-created_at', )

class OrderItem(models.Model):
  order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
  product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
  price = models.IntegerField()
  quantity = models.IntegerField(default=1)

  def display_price(self):
    return self.price / 100.00
