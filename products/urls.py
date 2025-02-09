from django.urls import path
from .views import create_product, product_detail, product_list, edit_product, delete_product,user_products

app_name = 'products'

urlpatterns = [
    path('create/', create_product, name='create_product'),
    path('product_list/', product_list, name='product_list'),
    path('user_products/', user_products, name='user_products'),
    path('product_detail/<slug:slug>/', product_detail, name='product_detail'),
    path('product_update/<slug:slug>/', edit_product, name='product_update'),
    path('product_delete/<slug:slug>/', delete_product, name='product_delete'),
    
]