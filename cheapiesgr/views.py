from django.shortcuts import render
from django.conf import settings
from django.contrib import messages

def default_map(request):
    return render(request, 'map_default.html',
                  { 'mapbox_access_token' : settings.MAPBOX_ACCESS_TOKEN })

def profile(request):
    return render(request, 'profile.html', {})

def privacy(request):
    return render(request, 'privacy.html', {})

def index(request):
    return render(request, 'index.html', {})

def product(request):
    return render(request, 'product.html',
                  { 'mapbox_access_token' : settings.MAPBOX_ACCESS_TOKEN })

def search(request):
    return render(request, 'search.html', {})

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

def user_auth(request):
    return render(request, 'user_auth.html', {})

#User signup view
from .forms import UserRegistrationForm
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
from .forms import UserLoginForm
def signin(request):
    if request.method == 'POST':
        f = UserLoginForm(request.POST)
        if f.is_valid():
            messages.success(request, 'Συνδεθήκατε με επιτυχία!')
            return render(request, 'index.html', {})
    else:
        f = UserLoginForm()
    return render(request, 'signin.html', {'form': f})
