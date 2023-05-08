from django.urls import path
from . views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns=[
    path('',index),
    path('test/',testFunc),
    path('addproduct/',post_product),
    path('addcategory/',post_category),
    path('updateproduct/<int:product_id>',update_product),
    path('deleteproduct/<int:product_id>',delete_product),
    path('category/',show_category),
    path('updatecategory/<int:category_id>',update_category),
    path('deletecategory/<int:category_id>',delete_category),
    path('add_to_cart/<int:product_id>',add_to_cart),
    path('mycart',show_cart_item),
    path('deletecartitems/<int:cart_id>',remove_cart_item),
    path('orderitemform/<int:product_id>/<int:cart_id>', order_item_form),
    path('my_order',my_order,name="my_order"),
    path('allorder',all_order,name="allorder"),
    path('allordercompleted',all_order_completed,name="allordercompleted"),

    path('esewa_verify',esewa_verify),
    path('allproducts',all_products),
    path('allcategoryview',all_category_view),
    path('categoryproduct/<int:category_id>/', view_products_by_category, name='view_products_by_category'),
    path('rate/<int:product_id>/<int:rating>/',rate),
    path('allproductsdes',all_products_des),
    path('allproductsaes',all_products_aes),
    path('changestatus/<int:id>/<str:status>',change_status,name="changestatus"),
    path('change_status/<int:order_id>/', change_payment_status, name='change_payment_status'),
    path('about',about,name="about"),
    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)