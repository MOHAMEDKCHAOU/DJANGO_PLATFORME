from django.contrib import admin
from .models import Product
from .models import Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity')
    search_fields = ('name', 'category')
    list_filter = ('category',)

admin.site.register(Category)
