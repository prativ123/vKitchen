from django.contrib import admin
from products.models import *
from .models import *
# Register your models here.
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(Recommendation)