from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Registration
from .models import Category

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
    request.session['categories'] = list(Category.objects.all().values())
    print(request.session['categories'])

    return render(request, 'index.html', {})

def product(request):
    return render(request, 'product.html',
                  { 'mapbox_access_token' : settings.MAPBOX_ACCESS_TOKEN })

@csrf_exempt
def search(request):
    search_text = request.POST.get("search")
    results = Registration.objects.filter(product_description__contains=search_text)

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
