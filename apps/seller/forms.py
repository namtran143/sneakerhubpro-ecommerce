from django import forms
from apps.products.models import Product

class SellerProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'price', 'discount_percent', 'description', 'image', 'stock', 'is_featured', 'is_flash_sale']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }
