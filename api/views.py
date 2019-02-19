from django.shortcuts import render
from django.views.decorators.http import require_http_methods

@require_http_methods(['POST'])
def login(request):
    return None

@require_http_methods(['POST'])
def logout(request):
    return None


def get_products(request):
    return None

def get_shops(request):
    return None


def get_prices(request):
    return None
