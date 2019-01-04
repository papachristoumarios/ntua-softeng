import requests
import sys
import datetime
from .forms import *
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from geopy.distance import distance as geopy_distance
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis.measure import D
from django import template
from nominatim import Nominatim
from geopy.geocoders import Nominatim as geonom
import random
import os
nom = Nominatim()


def handle_uploaded_file(f, category_name):
    category_name = category_name.replace(' ', '-')
    fname = '{}_{}'.format(random.randint(0, 100), str(f))
    dest = 'media/supermarket_crawlers/{}/images/{}'.format(
        category_name, fname)
    with open(os.path.join(settings.MEDIA_ROOT, dest), 'wb+') as g:
        g.write(f.read())

    return dest


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
    registration = Registration.objects.get(pk=product_id)

    if request.method == 'POST':
        f = ReviewForm(request.POST)
        q = QuestionForm(request.POST)
        if f.is_valid():
            stars = f.cleaned_data['stars']
            rate_explanation = f.cleaned_data['rate_explanation']

            # TODO Change volunteer
            volunteer = Volunteer.objects.get(pk=1)

            rating = Rating(
                stars=stars,
                rate_explanation=rate_explanation,
                registration=registration,
                volunteer=volunteer,
                validity_of_this_rate=0
            )

            rating.save()
            messages.success(
                request, 'Καταχωρήθηκε η κριτική!')
        elif q.is_valid():
            question_text = q.cleaned_data['question']

            # TODO Change volunteer
            volunteer = Volunteer.objects.get(pk=1)

            question = Question(
                question_text=question_text,
                registration=registration,
                volunteer=volunteer
            )

            question.save()
        return redirect('product/?productId={}'.format(product_id))
    else:
        f = ReviewForm()
        q = QuestionForm()


    return render(request, 'product.html', {
        'lat': lat,
        'lon': lon,
        'product': product,
        'plat': product_loc.y,
        'plon': product_loc.x,
        'distance': distance(product.location, client_loc),
        'form' : f,
        'qform' : q,
    })


def location(ip):
    g = GeoIP2()
    return g.geos(ip)



def distance(a, b):
    meters = geopy_distance(a, b).meters
    return Distance(m=meters).km


def order_by_distance(results):
    results.sort(key=lambda x: x[1])
    return results


def order_by_rating(results):
    results.sort(key=lambda x: 0 if x[0].stars is None else -x[0].stars)
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
        reg_data = Registration.objects.filter(
            category__id=category_id)[:limit]
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

        reg_data = Registration.objects.filter(
            product_description__contains=search_text,
            price__gte=pmin,
            price__lte=pmax)

        if category != 'Όλες':
            reg_data = reg_data.filter(category__category_name=category)

        if limit > 0:
            reg_data = reg_data[:limit]

        if orderby == 'price':
            reg_data = reg_data.order_by('price')

    distances = [distance(r.location, client_loc) for r in reg_data]
    results = [(r, d) for r, d in zip(reg_data, distances)]

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
        'rmin': rmin,
        'pmin': pmin,
        'pmax': pmax,
        'dmax': dmax,
        'num_results': num_results,
        'num_pages': paginator.num_pages,
        'pages': infinite_scroll_paginator(paginator),
        'search_text': search_text,
        'lat': lat,
        'lon': lon
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
        f = AddProductForm(request.POST, request.FILES)
        if f.is_valid():

            price = f.cleaned_data['price']
            product_description = f.cleaned_data['description']
            new_location = f.cleaned_data['new_location']
            new_shop_name = f.cleaned_data['new_shop_name']
            new_shop_city = f.cleaned_data['new_shop_city']
            new_shop_street = f.cleaned_data['new_shop_street']
            new_shop_number = f.cleaned_data['new_shop_number']
            category_id = f.cleaned_data['category']
            category = Category.objects.get(pk=category_id)
            date_of_registration = datetime.datetime.today().strftime('%Y-%m-%d')
            image_url = handle_uploaded_file(
                request.FILES['img'], category.category_name)

            if len(new_location) > 0:
                print('Adding a new shop at', new_location)
                query = nom.query(new_location)[0]
                shop = Shop(
                    name=new_location,
                    address=query['display_name'],
                    city=query['display_name'],
                    location='POINT({} {})'.format(query['lon'], query['lat']),
                )
                shop.save()
            elif len(new_shop_name) > 0:
                print('Adding a new shop named', new_shop_name)
                geolocator = geonom(user_agent="cheapiesgr")
                location = geolocator.geocode(new_shop_street+" "+new_shop_number+" "+new_shop_city)
                if str(type(location)) == "<class 'NoneType'>":
                    print('Μη έγκυρη διεύθυνση.')
                    return render(request, 'addproduct.html',{'form':f, 'correct_address': False})
                shop = Shop(
                    name=new_shop_name,
                    address=new_shop_street+" "+new_shop_number,
                    city=new_shop_city,
                    location='POINT({} {})'.format(location.longitude, location.latitude),
                )
                shop.save()
            else:
                shop_id = f.cleaned_data['location']
                shop = Shop.objects.get(pk=shop_id)

            # TODO Change volunteer
            volunteer = Volunteer.objects.get(pk=1)

            new_product = Registration(
                product_description=product_description,
                price=price,
                date_of_registration=date_of_registration,
                volunteer=volunteer,
                shop=shop,
                category=category,
                image_url=image_url
            )

            new_product.save()

            messages.success(request, 'Η καταχώρηση ήταν επιτυχής')
            return render(request, 'index.html', {})
    else:
        f = AddProductForm()
    return render(request, 'addproduct.html', {'form': f})

    return render(request, 'addproduct.html', {})


def user_auth(request):
    return render(request, 'user_auth.html', {})


def answer(request):
    question_id = request.GET.get('questionId', 1)
    product_id = request.GET.get('productId', 1)
    # TODO Change volunteer
    volunteer = Volunteer.objects.get(pk=1)
    question = Question.objects.get(pk=int(question_id))

    if request.method == 'POST':
        f = AnswerForm(request.POST)
        if f.is_valid():
            answer_text = f.cleaned_data['answer']
            answer = Answer(
                answer_text=answer_text,
                volunteer=volunteer,
                question=question
            )

            answer.save()
            messages.success(
                request, 'Ο λογαριασμός δημιουργήθηκε με επιτυχία!')
            return redirect('product/?productId={}'.format(product_id))
    else:
        f = AnswerForm()
    return render(request, 'answer.html', {'form': f})


def signup(request):
    if request.method == 'POST':
        f = UserRegistrationForm(request.POST)
        if f.is_valid():
            # f.save()
            messages.success(
                request, 'Ο λογαριασμός δημιουργήθηκε με επιτυχία!')
            return render(request, 'index.html', {})
    else:
        f = UserRegistrationForm()
    return render(request, 'signup.html', {'form': f})


def signin(request):
    if request.method == 'POST':
        f = UserLoginForm(request.POST)
        if f.is_valid():
            messages.success(request, 'Συνδεθήκατε με επιτυχία!')
            return render(request, 'index.html', {})
    else:
        f = UserLoginForm()
    return render(request, 'signin.html', {'form': f})
