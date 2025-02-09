from django.urls import path
from .views import index, about_as


app_name = 'home'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about_as, name='about_as'),

]

