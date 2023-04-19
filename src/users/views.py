from multiprocessing import context
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import LoginForm
from products.models import *


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Account Created')
            return redirect('/register')
        else:
            messages.add_message(request,messages.ERROR,'please provide correct details')
            return render(request, 'users/register.html',{
                'form':form
            })
    context={
        'form':UserCreationForm
    }
    return render(request,'users/register.html',context)

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])

            if user is  not None:
                login(request,user)
                if user.is_staff:
                    return redirect('/admins/dashboard')
                else:
                    return redirect('/')
            else:
                messages.add_message(request,messages.ERROR, 'Please provide correct credentails ')
                return render(request,'users/login.html',{
                    'forms':form
                })

    form = LoginForm
    context = {
        'form': form
    }
    return render(request,'users/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('/login')

def homepage(request):
    products = Product.objects.all().order_by('-id')[:8]
   
    context = {
        'products':products,
    
    }
    return render(request, 'users/index.html',context)

def productpage(request):
    products = Product.objects.all().order_by('-id')
    user = request.user
    items = Cart.objects.filter(user=user)
    context = {
        'products':products,
        'items':items
    }
    return render(request,'users/products.html',context)


def product_details(request,product_id):
    products=Product.objects.get(id=product_id)
    context = {
        'products':products
    }
    return render(request,'users/productdetails.html',context)