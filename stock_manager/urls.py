"""stock_manager URL Configuration"""

from django import views
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from products.views import product_list
from stock_manager import settings

urlpatterns = [
    path('', product_list, name='home'),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)