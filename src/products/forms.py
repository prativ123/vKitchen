import imp
from django.forms import ModelForm,fields
from . models import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['quantity','payment_method','contact_no','address']
