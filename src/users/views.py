from multiprocessing import context
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import LoginForm
from products.models import *
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required


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

def homepage(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all().order_by('-id')[:8]
    for product in products:
        # rating = Rating.objects.filter(product=product, user=request.user).first()
        
        # product.user_rating = rating.rating if rating else 0
        context = {
        'products':products, 

    }
    return render(request, 'users/index.html',context)
# context

def rate(request: HttpRequest, product_id: int, rating: int) -> HttpResponse:
    product = Product.objects.get(id=product_id)
    Rating.objects.filter(product=product, user=request.user).delete()
    product.rating_set.create(user=request.user, rating=rating)
    return homepage(request)



def productpage(request):
    products = Product.objects.all().order_by('-id')
    user = request.user
    items = Cart.objects.filter(user=user)
    context = {
        'products':products,
        'items':items
    }
    return render(request,'users/products.html',context)




@login_required
def product_details(request: HttpRequest,product_id) -> HttpResponse:

    order = Order.objects.filter(product=product_id,user=request.user.id,status="Completed")
    order_status = False
    if order: 
        order_status = True

    products=Product.objects.get(id=product_id)
    rating = Rating.objects.filter(product=products, user=request.user).first()
        # product.avg_rating = product.average_rating()
    products.user_rating = rating.rating if rating else 0
    reviews = Review.objects.filter(product=products).order_by('-id')[:7] 
    context = {
        'products':products, 
        'reviews' : reviews,
        'order_status':order_status

    }
    return render(request, 'users/productdetails.html',context)





from .models import Review
from products.models import Product


@login_required
def add_reviews(request: HttpRequest,product_id)->HttpResponse:
    if request.method == "POST":
        user = request.user
        products = Product.objects.get(id=product_id)
        order = Order.objects.filter(product=product_id,user=request.user.id,status="Completed")
        order_status = False
        if order: 
            order_status = True
        review = request.POST.get("review")
        new_review = Review(user=user, product=products, review=review)
        new_review.save()
        messages.success(request, "Thank you for reviewing this item!")
        reviews = Review.objects.filter(product=products).order_by('-id')[:7] 
        context={
            'products':products, 
            'reviews' : reviews,
            'order_status':order_status
        }

    return redirect('users:product_details',order_status=order_status,product_id=product_id)





    


# def product_details(request: HttpRequest,product_id) -> HttpResponse:
#     products=Product.objects.get(id=product_id)
#     rating = Rating.objects.filter(product=products, user=request.user).first()
#         # product.avg_rating = product.average_rating()
#     products.user_rating = rating.rating if rating else 0
#     reviews = Review.objects.filter(product=products).order_by('-id')[:7] 
#     context = {
#         'products':products, 
#         'reviews' : reviews,

#     }
#     return render(request, 'users/productdetails.html',context)