"""
URL configuration for nordic_homes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from core.views import test_message
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('prueba/', TemplateView.as_view(template_name='prueba.html'), name='prueba'),
    path('google/<str:q>/', RedirectView.as_view(url=f'https://google.com/search?q=%(q)s'), name='google'),
    path('test-messages/', test_message, name='test-messages'),
    
    path('', include('core.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

