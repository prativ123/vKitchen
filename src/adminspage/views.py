from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from users.auth import admin_only
from products.models import *
from django.contrib.auth.models import User

@login_required
@admin_only
def admin_home(request):
    total_orders = Order.objects.all().count()
    total_completed = Order.objects.filter(status="Completed").count()
    total_users = User.objects.all().count()
    context = {
        "total_orders":total_orders, 
        "total_completed":total_completed,
        "total_users":total_users
    }
    return render(request,'admins/adminhome.html',context)