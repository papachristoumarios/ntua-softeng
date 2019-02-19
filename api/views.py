import json
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

AUTH_TOKEN_LABEL = 'X-OBSERVATORY-AUTH'

def unicode_response(data):
    """ Returns unicode response """
    return HttpResponse(json.dumps(data, ensure_ascii=False),
                        content_type="application/json")

@csrf_exempt
@require_http_methods(['POST'])
def create_user(request):
    return None

@csrf_exempt
@require_http_methods(['POST'])
def logout_user(request):
    token = request.POST[AUTH_TOKEN_LABEL]
    try:
        user = Token.objects.get(key=token).user
        user.auth_token.delete()
        return unicode_response({'message' : 'OK'})
    except:
        return unicode_response({'message' : 'Token not associated with user'})

@csrf_exempt
def product(request):
    return None

@csrf_exempt
def shop(request):
    return None


def price(request):
    return None
