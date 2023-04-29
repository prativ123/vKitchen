from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from products.models import Product,Order


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    posted_on = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.review 
    


class Notification(models.Model): 
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    timestamp = models.DateField(default=timezone.now)
    content = models.CharField(max_length=100,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    


    class Meta:
        ordering = ["-timestamp"]

    
    
    