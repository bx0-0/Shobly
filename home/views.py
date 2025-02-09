from django.shortcuts import render
from .models import Team


def index(request):
    
    return render(request, 'home.html')

def about_as(request):
    
    team = Team.objects.all()
    
    return render(request, 'about_as.html', {'team': team})