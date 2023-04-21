from django.urls import path
from . views import *

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
    path('my_order',my_order),
    path('allorder',all_order),
    path('esewa_verify',esewa_verify),
    path('allproducts',all_products),
    path('allcategoryview',all_category_view),
    path('category/<int:category_id>/', view_products_by_category, name='view_products_by_category'),
    path('rate/<int:product_id>/<int:rating>/', rate, name='rate_product'),
    

]