import json
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from rest_framework.authtoken.models import Token
from cheapiesgr.models import *

AUTH_TOKEN_LABEL = 'X-OBSERVATORY-AUTH'

def unicode_response(data, status=200):
    """ Returns unicode response """
    if status == 200:
        return HttpResponse(json.dumps(data, indent=4, ensure_ascii=False),
                            content_type="application/json", status=status)
    else:
        return HttpResponse(json.dumps(data, indent=4, ensure_ascii=False), status=status)



def build_list_from_queryset(query_set):
    result = []
    for x in query_set:
        result.append(x.serialize())
    return result

def query_api(request, objects, list_label):
    # Get arguments
    start = int(request.GET.get('start', 0))
    count = int(request.GET.get('count', 20))
    status = request.GET.get('status', 'ACTIVE')
    sort = request.GET.get('sort', 'id|DESC')
    total = objects.count()

    # Status
    if status == 'ACTIVE':
        status_result = objects.filter(withdrawn=False)
    elif status == 'WITHDRAWN':
        status_result = objects.filter(withdrawn=True)
    elif status == 'ALL':
        status_result = objects
    else:
        return unicode_response({'message' : 'Invalid status'}, status=400)

    # Sort
    if sort == 'id|DESC':
        sort_result = status_result.order_by('-id')
    elif sort == 'id|ASC':
        sort_result = status_result.order_by('id')
    elif sort == 'name|ASC':
        if list_label == 'shops':
            sort_result = status_result.order_by('name')
        elif list_label == 'products':
            sort_result = status_result.order_by('product_description')
    elif sort == 'name|DESC':
        if list_label == 'shops':
            sort_result = status_result.order_by('-name')
        elif list_label == 'products':
            sort_result = status_result.order_by('-product_description')
    else:
        return unicode_response({'message' : 'Invalid sort criterion'}, status=400)


    # Paginate
    try:
        paginator = Paginator(sort_result, count)
        result = paginator.page(start + 1)
    except:
        return unicode_response({'message' : 'Invalid pagination'}, status=400)


    data = {
        'start' : start,
        'count' : count,
        'total' : total,
        list_label : build_list_from_queryset(result)
    }
    return data

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
        return unicode_response({'message' : 'Token not associated with user'}, status=400)

@csrf_exempt
def product(request):
    return None

@csrf_exempt
def shop(request, shop_id='all'):

    if request.method == 'GET':
        if shop_id == 'all':
            return unicode_response(query_api(request, Shop.objects.all(), 'shops'))
        else:
            shop = Shop.objects.get(pk=int(shop_id))
            return unicode_response(shop.serialize())


def price(request):
    return None
