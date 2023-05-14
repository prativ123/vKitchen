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
from users.models import Recommendation

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

    if request.user.is_authenticated:

        recommendeds = Recommendation.objects.filter(user=request.user)
        recommend_list = [a.product.id for a in recommendeds]
        print(recommend_list)
        recommendation_products = Product.objects.filter(id__in=recommend_list )[:8]

    # for product in products:
        # rating = Rating.objects.filter(product=product, user=request.user).first()
        
        # product.user_rating = rating.rating if rating else 0
        print(recommendation_products)
        context = {
        'products':products, 
        'recommendations':recommendation_products
        }
    else:
        context ={
            "products":products
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

    print(request.user)
    
    products=Product.objects.get(id=product_id)
    category = Category.objects.get(id=products.category.id)
    products_list = Product.objects.filter(category=category)[:4]

    for i in products_list: 
        recommendation = Recommendation(user=request.user,product=i)
        recommendation.save()

    
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



from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView

from .models import Review,Notification
from products.models import Product



@login_required
def add_reviews(request: HttpRequest,product_id)->HttpResponse:
    if request.method == "POST":
        user = request.user
        products = Product.objects.get(id=product_id)

        review = request.POST.get("review")
        new_review = Review(user=user, product=products, review=review)
        new_review.save()
        messages.success(request, "Thank you for reviewing this item!")
        reviews = Review.objects.filter(product=products).order_by('-id')[:7] 
        context={
            'products':products, 
            'reviews' : reviews,
            
        }

    return redirect('users:product_details',product_id=product_id)



from django.utils import timezone
class NotificationListView(LoginRequiredMixin,ListView):
    model = Notification
    template_name = 'notification_list.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add created_date to the context
        context['now'] = timezone.now()
        return context
    


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

# from django.shortcuts import render, redirect
# from django.http import Http404
# from django.db.models import Q
# from products.models import Rating, Product
# import pandas as pd

# def get_similar_items(product_id, rating, corr_matrix):
#     similar_ratings = corr_matrix[product_id] * (rating - 2.5)
#     similar_ratings = similar_ratings.sort_values(ascending=False)
#     return similar_ratings

# def recommend_items(request, product_id):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     if not request.user.is_active:
#         raise Http404

#     ratings = pd.DataFrame(list(Rating.objects.all().values()))

#     num_users = ratings.user_id.unique().shape[0]
#     current_user_id = request.user.id

#     # If new user hasn't rated any items
#     if current_user_id > num_users:
#         item = Product.objects.get(id=product_id)

#         new_rating = Rating(user=request.user, item=item, score=0)
#         new_rating.save()

#     user_ratings = ratings.pivot_table(index=['user_id'], columns=['product_id'], values='score')
#     user_ratings = user_ratings.fillna(0, axis=1)
#     corr_matrix = user_ratings.corr(method='pearson')

#     user = pd.DataFrame(list(Rating.objects.filter(user=request.user).values())).drop(['user_id', 'id'], axis=1)
#     user_filtered = [tuple(x) for x in user.values]
#     item_ids_watched = [each[0] for each in user_filtered]

#     similar_items = pd.DataFrame()
#     for item, rating in user_filtered:
#         similar_items = similar_items.append(get_similar_items(item, rating, corr_matrix), ignore_index=True)

#     item_ids = list(similar_items.sum().sort_values(ascending=False).index)
#     item_ids_recommend = [each for each in item_ids if each not in item_ids_watched]
#     recommended_items = list(Product.objects.filter(id__in=item_ids_recommend).order_by('-rating')[:10])

#     context = {'recommended_items': recommended_items}
#     return render(request, 'recommendations.html', context)


# import csv
# from itertools import combinations
# from collections import defaultdict
# from django.shortcuts import render

# def read_csv(filename):
#     with open(filename, 'r') as file:
#         reader = csv.reader(file)
#         next(reader)  # skip header row
#         data = [row for row in reader]
#         return data

# # function to get the frequent item sets using Apriori algorithm
# def get_frequent_itemsets(transactions, min_support):
#     item_counts = defaultdict(int)
#     for transaction in transactions:
#         for item in transaction:
#             item_counts[item] += 1

#     num_transactions = len(transactions)
#     min_count = num_transactions * min_support
#     frequent_items = {item: count for item, count in item_counts.items() if count >= min_count}
#     frequent_itemsets = [{item} for item in frequent_items]

#     k = 2
#     while True:
#         candidate_itemsets = set()
#         for itemset in frequent_itemsets:
#             for item in frequent_items:
#                 if item not in itemset:
#                     candidate_itemsets.add(itemset | {item})

#         item_counts = defaultdict(int)
#         for transaction in transactions:
#             for itemset in candidate_itemsets:
#                 if itemset.issubset(transaction):
#                     item_counts[itemset] += 1

#         frequent_itemsets = [itemset for itemset, count in item_counts.items() if count >= min_count]
#         if len(frequent_itemsets) == 0:
#             break

#         frequent_items = set()
#         for itemset in frequent_itemsets:
#             frequent_items |= itemset

#         k += 1

#     return frequent_itemsets

# def get_recommendations(request):
#     # read product data from CSV file
#     products = read_csv('data/product_data.csv')
    
#     # get user's past orders
#     past_orders = Order.objects.filter(user=request.user, status='Completed')

#     # extract items from past orders
#     transactions = []
#     for order in past_orders:
#         order_items = Order.objects.filter(order=order)
#         item_names = [product[1] for product in products if product[0] in [order_item.product_id for order_item in order_items]]
#         transactions.append(set(item_names))
        
#     # get frequent item sets using Apriori algorithm
#     min_support = 0.2
#     frequent_itemsets = get_frequent_itemsets(transactions, min_support)

#     # convert frequent itemsets into a dictionary
#     item_counts = defaultdict(int)
#     for itemset in frequent_itemsets:
#         for item in itemset:
#             item_counts[item] += 1

#     # sort items by frequency
#     sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
#     context = {'recommendations': sorted_items}
#     return render(request, 'users/recommendations.html', context)

