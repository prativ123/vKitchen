import imp
from django import forms
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

class ChangePaymentStatusForm(forms.Form):
    PAYMENT_STATUS_CHOICES = (
        (True, 'Paid'),
        (False, 'Unpaid'),
    )
    payment_status = forms.ChoiceField(choices=PAYMENT_STATUS_CHOICES, required=True)