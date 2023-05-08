from django.urls import path
from . views import *
from products.views import *
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "users"

urlpatterns=[
    path('register/', register_user),
    path('login/', login_user),
    path('logout/',logout_user),
    path('',homepage, name='homepage'),
    path('allproducts/',productpage),
    path('productdetails/<int:product_id>', product_details, name='product_details'),
    path('rate/<int:product_id>/<int:rating>/',rate),
    path('postReview/<int:product_id>',add_reviews, name='add_reviews'),
    path('notification/',NotificationListView.as_view(),name="notification"),
    # path('recommendations/<int:product_id>/', views.recommend_items, name='recommendations'),
    # path('recommend/',get_recommendations, name='get_recommendations'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)