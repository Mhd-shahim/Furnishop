from django import forms
from .models import Product,Category,Coupon

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'
