import requests
import sys
from .forms import UserRegistrationForm
from .forms import AddProductForm
from .forms import UserLoginForm
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Category
from .models import Registration
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from geopy.distance import distance as geopy_distance
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis.measure import D

def default_map(request):
    return render(request, 'map_default.html', {})

def profile(request):
    return render(request, 'profile.html', {})

def privacy(request):
    return render(request, 'privacy.html', {})

def index(request):
    request.session['categories'] = list(Category.objects.all().values())

    return render(request, 'index.html', {})

def product(request):
    product_id = int(request.GET.get('productId', 0))
    lat = request.session.get('lat', 0)
    lon = request.session.get('lon', 0)
    client_loc = Point(lon, lat, srid=4326)


    product = Registration.objects.get(pk=product_id)
    product_loc = product.location

    return render(request, 'product.html', {
        'lat' : lat,
        'lon' : lon,
        'product' : product,
        'plat' : product_loc.y,
        'plon' : product_loc.x,
        'distance' : distance(product.location , client_loc)
    })

def location(ip):
    g = GeoIP2()
    return g.geos(ip)

def distance(a, b):
    meters = geopy_distance(a, b).meters
    return Distance(m=meters).km

def order_by_distance(results):
    results.sort(key = lambda x: x[1])
    return results

def order_by_rating(results):
    results.sort(key = lambda x: 0 if x[0].stars == None else -x[0].stars)
    return results

def apply_search_filters(results, dmax, rmin):
    results = filter(lambda x: x[0].stars >= rmin, results)
    return list(results)

def infinite_scroll_paginator(paginator):
    for i in range(1, paginator.num_pages + 1):
        yield paginator.page(i)


@csrf_exempt
def search(request):
    if request.method == 'GET':

        category_id = request.GET.get('categoryId')
        orderby = 'price'
        dmax = sys.maxsize
        dmin = - sys.maxsize
        rmin = 0
        pmin = 0
        rmax = 5
        limit = 100
        pmax = sys.maxsize
        search_text = ''
        lat = request.session.get('lat', 0)
        lon = request.session.get('lon', 0)
        reg_data = Registration.objects.filter(category__id=category_id)[:limit]
        client_loc = Point(lon, lat, srid=4326)
    else:
        search_text = request.POST.get('search')

        category = request.POST.get('category-select', 'Όλες')

        try:
            lat = float(request.POST.get('lat'))
            lon = float(request.POST.get('lon'))
            request.session['lat'] = lat
            request.session['lon'] = lon
        except ValueError:
            lat = lon = 0
        except TypeError:
            lat = lon = 0
        finally:
            client_loc = Point(lon, lat, srid=4326)


        try:
            orderby = request.POST.get('orderby')
        except ValueError:
            orderby = 'price'

        try:
            rmin = int(request.POST.get('rmin'))
        except ValueError:
            rmin = 0
        except TypeError:
            rmin = 0


        try:
            pmin = float(request.POST.get('pmin'))
        except ValueError:
            pmin = 0
        except TypeError:
            pmin = 0

        try:
            pmax = float(request.POST.get('pmax'))
        except ValueError:
            pmax = sys.maxsize
        except TypeError:
            pmax = sys.maxsize

        try:
            dmax = float(request.POST.get('dmax'))
        except ValueError:
            dmax = sys.maxsize
        except TypeError:
            dmax = sys.maxsize

        try:
            limit = float(request.POST.get('limit'))
        except ValueError:
            limit = -1
        except TypeError:
            limit = -1



        reg_data = Registration.objects.filter(product_description__contains=search_text,
                        price__gte=pmin,
                        price__lte=pmax)

        if category != 'Όλες':
            reg_data = reg_data.filter(category__category_name=category)

        if limit > 0:
            reg_data = reg_data[:limit]

        if orderby == 'price':
            reg_data = reg_data.order_by('price')

    distances = [distance(r.location ,client_loc) for r in reg_data]
    results = [(r,d) for r, d in zip(reg_data, distances)]

    if orderby == 'rating':
        results = order_by_rating(results)
    elif orderby == 'distance':
        results = order_by_distance(results)

    # apply search filters
    if request.method == 'POST':
        results = apply_search_filters(results, dmax=dmax, rmin=rmin)

    num_results = len(results)
    # paginate
    paginator = Paginator(results, 20)


    return render(request, 'search.html', {
        'rmin' : rmin,
        'pmin' : pmin,
        'pmax' : pmax,
        'dmax' : dmax,
        'num_results': num_results,
        'num_pages' : paginator.num_pages,
        'pages' : infinite_scroll_paginator(paginator),
        'search_text' : search_text,
        'lat' : lat,
        'lon' : lon
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
    if request.method == 'POST':
        f = AddProductForm(request.POST)
        if f.is_valid():
            print('post!')
            print(f.cleaned_data['new_location'])
            print(f.cleaned_data['location'])
            print(f.cleaned_data['category'])


            messages.success(request, 'Η καταχώρηση ήταν επιτυχής')
            return render(request, 'index.html', {})
    else:
        f = AddProductForm()
    return render(request, 'addproduct.html', {'form': f})

    return render(request, 'addproduct.html', {})

def user_auth(request):
    return render(request, 'user_auth.html', {})

def signup(request):
    if request.method == 'POST':
        f = UserRegistrationForm(request.POST)
        if f.is_valid():
            #f.save()
            messages.success(request, 'Ο λογαριασμός δημιουργήθηκε με επιτυχία!')
            return render(request, 'index.html', {})
    else:
        f = UserRegistrationForm()
    return render(request, 'signup.html', {'form': f})

#User login view
def signin(request):
    if request.method == 'POST':
        f = UserLoginForm(request.POST)
        if f.is_valid():
            messages.success(request, 'Συνδεθήκατε με επιτυχία!')
            return render(request, 'index.html', {})
    else:
        f = UserLoginForm()
    return render(request, 'signin.html', {'form': f})
