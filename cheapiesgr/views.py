from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Registration
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from geopy.distance import distance as geopy_distance

def default_map(request):
    return render(request, 'map_default.html',
                  { 'mapbox_access_token' : settings.MAPBOX_ACCESS_TOKEN })

def signup(request):
    return render(request, 'signup.html', {})

def profile(request):
    return render(request, 'profile.html', {})

def privacy(request):
    return render(request, 'privacy.html', {})

def signin(request):
    return render(request, 'signin.html', {})

def index(request):
    return render(request, 'index.html', {})

def product(request):
    return render(request, 'product.html',
                  { 'mapbox_access_token' : settings.MAPBOX_ACCESS_TOKEN })

def location(ip):
    g = GeoIP2()
    return g.geos(ip)

def distance(a, b):
    meters = geopy_distance(a, b).meters
    return Distance(m=meters).km

@csrf_exempt
def search(request):
    search_text = request.POST.get("search")
    reg_data = Registration.objects.filter(product_description__contains=search_text)
    client_ip = '62.75.78.22' # Example
    '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request.META.get('REMOTE_ADDR')
    '''
    client_loc = location(client_ip)

    distances = [distance(r.get_location(),client_loc) for r in reg_data]
    results = [[r,d] for r in reg_data for d in distances]
    print(distances)
    return render(request, 'search.html', {
        'results' : results,
        'search_text' : search_text,
    })

def report(request):
    return render(request, 'report.html', {})

def newproduct1(request):
    return render(request, 'newproduct1.html', {})

def newproduct2(request):
    return render(request, 'newproduct2.html', {})

def newproduct3(request):
    return render(request, 'newproduct3.html', {})

def addproduct(request):
    return render(request, 'addproduct.html', {})
