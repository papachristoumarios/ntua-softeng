from django.shortcuts import render
from django.conf import settings


def default_map(request):
    return render(request, 'map_default.html',
                  { 'mapbox_access_token' : settings.MAPBOX_ACCESS_TOKEN })

def signup(request):
    return render(request, 'signup.html', {})

def index(request):
    return render(request, 'index.html', {})    
