import imp
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *
from django.core import validators


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    stock = models.IntegerField()
    image = models.FileField(upload_to='static/uploads', null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    
    def average_rating(self) -> float:
        return Rating.objects.filter(products=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return f"{self.product_name}: {self.average_rating()}"
    
class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_data = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    PAYMENT = (
        ('Cash on Delivery','Cash on Delivery'),
        ('Esewa','Esewa'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField(null=True)
    status = models.CharField(default='Pending', max_length=200)
    payment_method = models.CharField(max_length=200,choices=PAYMENT)
    payment_status = models.BooleanField(default=False,null=True,blank=True)
    contact_no = models.CharField(validators=[MinLengthValidator(9),MaxLengthValidator(10)], max_length=10)
    address = models.CharField(max_length=200, null=True)
    created_date = models.DateTimeField(auto_now_add=True)


from django.db.models import Avg

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.products}: {self.rating}"