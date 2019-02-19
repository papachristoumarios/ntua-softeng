import json
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse

def unicode_response(data):
    """ Returns unicode response """
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")

@require_http_methods(['POST'])
def login(request):
    return None

@require_http_methods(['POST'])
def logout(request):
    return unicode_response({'δσαFoo' : 'ok'})


def get_products(request):
    return None

def get_shops(request):
    return None


def get_prices(request):
    return None
