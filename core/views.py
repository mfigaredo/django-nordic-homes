from django.shortcuts import render, redirect
from django.http import HttpResponse
from product.models import Product, Category
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as dj_login
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.views import LogoutView, LoginView
from .forms import SignUpForm
from django_htmx.http import HttpResponseClientRefresh
from django.contrib import messages


# Create your views here.
def frontpage(request):
  products = Product.objects.all()[0:8]
  return render(request, 'core/frontpage.html', {'products': products})

def shop(request):
  active_category = request.GET.get('category', '')
  products = Product.objects.all() if not active_category else Product.objects.filter(category__slug=active_category)
  categories = Category.objects.annotate(num_products=Count('products')).filter(num_products__gt=0)
  query = request.GET.get('query')
  if query:
    products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

  context = {
    'products': products, 
    'categories': categories, 
    'active_category': active_category,
  }
  return render(request, 'core/shop.html', context)

def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save()
      dj_login(request, user)
      return redirect('frontpage')
    print(form.errors)
    # print(form.fields['username']['errors'])
  else:
    form = SignUpForm() 
  return render(request, 'core/signup.html', {'form': form, })

def login(request):
  return render(request, 'core/login.html')

@method_decorator([login_required, require_POST], name='dispatch')
class MyLogoutView(LogoutView):

  def dispatch(self, *args, **kwargs):
    response = super().dispatch(*args, **kwargs)
    messages.success(self.request, 'You have been logged out.')
    return HttpResponseClientRefresh()

# @method_decorator(require_GET, name='dispatch')
class MyLoginView(LoginView):
  
  template_name='core/login.html' 

  def dispatch(self, *args, **kwargs):
    response = super().dispatch(*args, **kwargs)

    if self.request.method == 'POST' and self.request.user:
      messages.success(self.request, 'Hello <strong>%s</strong>, welcome! You are logged in.' % self.request.user.username)

    return response

def test_message(request):
  messages.success(request, 'This is a SUCCESS message!')
  messages.error(request, 'This is a ERROR message!')
  messages.warning(request, 'This is a WARNING message!')
  messages.info(request, 'This is a INFO message!')
  messages.debug(request, 'This is a DEBUG message!')
  # print(messages.DEFAULT_TAGS)
  return redirect('frontpage')

@login_required
def myaccount(request):
  return render(request, 'core/myaccount.html', {})

@login_required
def edit_myaccount(request):
  if request.method == 'POST':

    user = request.user
    user.first_name = request.POST.get('first_name') or user.first_name
    user.last_name = request.POST.get('last_name') or user.last_name
    user.username = request.POST.get('username') or user.username
    user.email = request.POST.get('email') or user.email
    user.save()
    
    return redirect('my-account')
    # first_name = request.POST.get('first_name')
  return render(request, 'core/edit_myaccount.html', {})