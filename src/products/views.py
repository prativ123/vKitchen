from email import message
from multiprocessing import context
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse

from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.auth import admin_only


# Create your views here.
@login_required
@admin_only
def index(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products/index.html', context)

def testFunc(request):
    return HttpResponse('this is just the test function')

@login_required
@admin_only
def post_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'product added')
            return redirect('/products/addproduct')
        else:
            messages.add_message(request,messages.ERROR,'please verify forms fields. ')
            return render(request,'products/addproduct.html',{
                'form':form
            })
    context = {
        'form':ProductForm
    }

    return render(request, 'products/addproduct.html',context)

@login_required
@admin_only
def post_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'category added')
            return redirect('/products/addcategory')
        else:
            messages.add_message(request,messages.ERROR,'please verify forms fields. ')
            return render(request,'products/addcategory.html',{
                'form':form
            })
    context = {
        'form':CategoryForm
    }

    return render(request, 'products/addcategory.html',context)

@login_required
@admin_only
def update_product(request,product_id):
    instance = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'product updated')
            return redirect('/products')
        else:
            messages.add_message(request,messages.ERROR,'please verify forms fields. ')
            return render(request,'products/updateproduct.html',{
                'form':form
            })
    context={
        'form':ProductForm(instance=instance)
    }

    return render(request,'products/updateproduct.html',context)

@login_required
@admin_only
def delete_product(request,product_id):
        product=Product.objects.get(id=product_id)
        product.delete()
        messages.add_message(request,messages.SUCCESS,'product deleted')
        return redirect('/products')

@login_required
@admin_only
def show_category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'products/allcategory.html', context)

@login_required
@admin_only
def update_category(request,product_id):
    instance = Category.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'product updated')
            return redirect('/products')
        else:
            messages.add_message(request,messages.ERROR,'please verify forms fields. ')
            return render(request,'products/updateproduct.html',{
                'form':form
            })
    context={
        'form':ProductForm(instance=instance)
    }

    return render(request,'products/updateproduct.html',context)

@login_required
@admin_only
def delete_product(request,product_id):
        product=Product.objects.get(id=product_id)
        product.delete()
        messages.add_message(request,messages.SUCCESS,'product deleted')
        return redirect('/products')

@login_required
@admin_only
def update_category(request,category_id):
    instance = Category.objects.get(id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'category updated')
            return redirect('/products/category')
        else:
            messages.add_message(request,messages.ERROR,'please verify forms fields. ')
            return render(request,'products/updatecategory.html',{
                'form':form
            })
    context={
        'form':CategoryForm(instance=instance)
    }

    return render(request,'products/updatecategory.html',context)

@login_required
@admin_only
def delete_category(request,category_id):
        category=Category.objects.get(id=category_id)
        category.delete()
        messages.add_message(request,messages.SUCCESS,'category deleted')
        return redirect('/products/category')


@login_required
def add_to_cart(request,product_id):
    user=request.user
    product = Product.objects.get(id=product_id)
    
    check_item_presence = Cart.objects.filter(user=user,product=product)
    if check_item_presence:
        messages.add_message(request,messages.ERROR,'Product is already present in the cart')
        return redirect('/allproducts')

    else:
        cart = Cart.objects.create(product=product,user=user)
        if cart:
            messages.add_message(request,messages.SUCCESS,'Product added to cart')
            return redirect('/products/mycart')
        else:
            messages.add_message(request,messages.ERROR,'Unable to add item to cart')

@login_required
def show_cart_item(request):
    user = request.user
    items=Cart.objects.filter(user=user)
    context={
        'items':items
    }
    return render(request,'users/mycart.html',context)

@login_required
def remove_cart_item(request,cart_id):
    item = Cart.objects.get(id=cart_id)
    item.delete()
    messages.add_message(request,messages.SUCCESS,'Item remove from the cart')
    return redirect('/products/mycart')

@login_required
def order_item_form(request,product_id,cart_id):
    user=request.user
    product=Product.objects.get(id=product_id)
    cart_item = Cart.objects.get(id=cart_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity=request.POST.get('quantity')
            price=product.product_price
            total_price = int(quantity)*int(price)
            contact_no = request.POST.get('contact_no')
            address = request.POST.get('address')
            payment_method = request.POST.get('payment_method')
            payment_status = request.POST.get('payment_status')
            order = Order.objects.create(
                product = product,
                user=user,
                quantity=quantity,
                total_price=total_price,
                contact_no = contact_no,
                address=address,
                payment_method=payment_method,
                payment_status=payment_status,
            )
            if order.payment_method == 'Cash on Delivery':
                cart = Cart.objects.get(id=cart_id)
                cart.delete()
                messages.add_message(request,messages.SUCCESS,'Order Successful')
                return redirect('/products/my_order')

            elif order.payment_method == 'Esewa':
                context={
                    'order':order,
                    'cart': cart_item
                }
                return render(request,'users/esewa_payment.html',context)
            else:
                message.add_message(request,messages.ERROR,'Something went wrong')
                return render(request,'users/orderform.html',context)

    context = {
        'form': OrderForm
    }
    return render(request, 'users/orderform.html', context)

@login_required
def my_order(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    items = Cart.objects.filter(user=user)
    context = {
        'orders':orders,
        'items':items
    }
    return render(request,'users/my_order.html',context)

@login_required
@admin_only
def all_order(request):
    items = Order.objects.all()
    context = {
        'items':items
    }
    return render(request,'products/allorders.html',context)

import requests as req
def esewa_verify(request):
    import xml.etree.ElementTree as ET
    o_id = request.GET.get('oid')
    amount = request.GET.get('amt')
    refId = request.GET.get('refId')
    url ="https://uat.esewa.com.np/epay/transrec"
    d = {
    'amt': amount,
    'scd': 'EPAYTEST',
    'rid': refId,
    'pid': o_id,
    
    }
    resp = req.post(url, d)
    root = ET.fromstring(resp.content)
    status = root[0].text.strip()
    if status == 'Success':
        order_id = o_id.split("_")[0]
        order = Order.objects.get(id=order_id)
        order.payment_status = True
        order.save()
        cart_id=o_id.split("_")[1]
        cart = Cart.objects.get(id=cart_id)
        cart.delete()
        messages.add_message(request,messages.SUCCESS,'Payment Successful')
        return redirect('/products/mycart')
    else:
        messages.add_message(request,messages.ERROR,'Unable to make Payment')
        return redirect('/products/mycart')