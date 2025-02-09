from django.urls import path
from .views import cart, add_to_cart, complete_order, remove_from_cart, increase_quantity, decrease_quantity, refund_failed_order

app_name = 'cart'

urlpatterns = [
    path('view/', cart, name='cart'),
    path('add/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path('remove/<slug:slug>/', remove_from_cart, name='remove_from_cart'),
    path('increase/<slug:slug>/', increase_quantity, name='increase_quantity'),
    path('decrease/<slug:slug>/', decrease_quantity, name='decrease_quantity'),
    path('complete_order/', complete_order, name='complete_order'),
    path('failed-order/<int:id>/refund/', refund_failed_order, name='refund_failed_order'),
]