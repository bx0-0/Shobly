from django.urls import path
from .views import predict

app_name = 'ai_predict'

urlpatterns = [
    path('predict/', predict, name='predict'),
    
]