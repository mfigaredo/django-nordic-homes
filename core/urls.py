from django.urls import path
from core.views import frontpage, signup, MyLoginView, MyLogoutView, shop, myaccount, edit_myaccount
from product.views import product
from django.views.generic import TemplateView

urlpatterns = [
  path('', frontpage, name='frontpage'),
  path('signup/', signup, name='signup'),
  path('logout/', MyLogoutView.as_view(), name='logout'),
  path('login/', MyLoginView.as_view(), name='login'),
  path('shop/', shop, name='shop'),
  path('about/', TemplateView.as_view(template_name='core/about.html'), name='about'),
  path('shop/<slug:slug>/', product, name='product'),
  path('my-account/', myaccount, name='my-account'),
  path('my-account/edit/', edit_myaccount, name='edit_my-account'),
]
