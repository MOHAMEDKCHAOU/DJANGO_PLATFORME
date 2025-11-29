from django import forms
from .models import Order, Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'quantity', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),

        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }
        

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
