from django.urls import path
from .views import create_product, product_detail

app_name = 'products'

urlpatterns = [
    path('create/', create_product, name='create_product'),
    path('product_detail/<slug:slug>/', product_detail, name='product_detail'),
    
]