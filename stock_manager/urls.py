"""stock_manager URL Configuration"""

from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from stock_manager import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)