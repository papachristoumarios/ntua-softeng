import datetime
import json
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from rest_framework.authtoken.models import Token
from cheapiesgr.models import *
from django.contrib.gis.geos import Point
from django.http import QueryDict


AUTH_TOKEN_LABEL = 'HTTP_X_OBSERVATORY_AUTH'

def unicode_response(data, status=200):
    """ Returns unicode response """
    if status == 200:
        return HttpResponse(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False),
                            content_type="application/json", status=status)
    else:
        return HttpResponse(json.dumps(data, indent=4, ensure_ascii=False), status=status)

def build_list_from_queryset(query_set):
    result = []
    for x in query_set:
        result.append(x.serialize())
    return result

def authenticate_token(request):
    try:
        user = Token.objects.get(key=request.META[AUTH_TOKEN_LABEL]).user
        return True
    except:
        return False

def is_superuser(request):
    user = Token.objects.get(key=request.META[AUTH_TOKEN_LABEL]).user
    return user.is_superuser

def get_request_data(request):
    temp = dict(QueryDict(request.body))
    data = dict([(key, val[0]) for key, val in temp.items()])
    return data


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
        sort_result = status_result.order_by('name')
    elif sort == 'name|DESC':
        sort_result = status_result.order_by('-name')
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

def create_or_update_shop(request, shop_id):
    try:
        Shop.objects.update_or_create(
            id=shop_id,
            name=request.POST['name'],
            address=request.POST['address'],
            location='POINT({} {})'.format(
                request.POST['lng'],
                request.POST['lat']
            ),
            tags=json.dumps(request.POST['tags'], ensure_ascii=True)
        )

        return unicode_response({'message' : 'Shop created sucessfully'}, status=200)
    except:
        return unicode_response({'message' : 'Parameters not valid'}, status=400)


def patch_shop(request, shop_id):
    try:
        shop = Shop.objects.get(pk=shop_id)
        data = get_request_data(request)
        if 'name' in data:
            shop.name = data['name']
        if 'address' in data:
            shop.address = data['address']
        if 'tags' in data:
            shop.tags = json.dumps(data['tags'])
        if 'withdrawn' in data:
            shop.withdrawn = data['withdrawn']
        if 'lng' in data or 'lat' in data:
            print(shop.location)
            lat = data.get('lat', shop.location.y)
            lon = data.get('lng', shop.location.x)
            shop.location = 'SRID=4326;POINT({} {})'.format(lon, lat)
        shop.save()
        return unicode_response({'message' : 'Shop patched sucessfully'}, status=200)
    except:
        return unicode_response({'message' : 'Parameters not valid'}, status=400)


def remove_shop(request, shop_id):
    try:
        shop = Shop.objects.get(id=shop_id)
        if is_superuser(request):
            shop.delete()
            return unicode_response({'message' : 'Removal successfull'})
        else:
            shop.withdrawn = True
            shop.save()
            return unicode_response({'message' : 'Withdrawal successfull'})

    except:
        return unicode_response({'message' : 'Parameters not valid'}, status=400)


def parse_date(date_str):
    format_str = '%Y-%m-%d'
    return datetime.datetime.strptime(date_str, format_str)


def create_price(request):
    price = RegistrationPrice(
        date_from=parse_date(request.POST['dateFrom']),
        date_to=parse_date(request.POST['dateTo']),
        price=request.POST['price'],
        shop_id=int(request.POST['shopId']),
        registration_id=int(request.POST['productId'])
    )
    price.save()
    return unicode_response({'message' : 'Price creation sucessfull'})

# TODO
def query_prices(request):
    return None


def remove_product(request, product_id):
    try:
        registration = Registration.objects.get(id=product_id)
        if is_superuser(request):
            registration.delete()
            return unicode_response({'message' : 'Removal successfull'})
        else:
            registration.withdrawn = True
            registration.save()
            return unicode_response({'message' : 'Withdrawal successfull'})
    except:
        return unicode_response({'message' : 'Parameters not valid'}, status=400)



@csrf_exempt
@require_http_methods(['POST'])
def create_user(request):
    return None

@csrf_exempt
@require_http_methods(['POST'])
def logout_user(request):
    token = request.META[AUTH_TOKEN_LABEL]
    try:
        user = Token.objects.get(key=token).user
        user.auth_token.delete()
        return unicode_response({'message' : 'OK'})
    except:
        return unicode_response({'message' : 'Token not associated with user'}, status=400)

@csrf_exempt
@require_http_methods(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def shop(request, shop_id='all'):
    if request.method == 'GET':
        if shop_id == 'all':
            return unicode_response(query_api(request, Shop.objects.all(), 'shops'))
        else:
            shop = Shop.objects.get(pk=int(shop_id))
            return unicode_response(shop.serialize())
    elif request.method in ['POST', 'PUT']:
        if shop_id == 'all':
            return unicode_response({'message' : 'Invalid Request'}, status=400)
        elif not authenticate_token(request):
            return unicode_response({'message' : 'Forbidden'}, status=403)
        else:
            return create_or_update_shop(request, int(shop_id))
    elif request.method == 'PATCH':
        if shop_id == 'all':
            return unicode_response({'message' : 'Invalid Request'}, status=400)
        elif not authenticate_token(request):
            return unicode_response({'message' : 'Forbidden'}, status=403)
        else:
            return patch_shop(request, int(shop_id))
    elif request.method == 'DELETE':
        if shop_id == 'all':
            return unicode_response({'message' : 'Invalid Request'}, status=400)
        elif not authenticate_token(request):
            return unicode_response({'message' : 'Forbidden'}, status=403)
        else:
            return remove_shop(request, int(shop_id))


@csrf_exempt
@require_http_methods(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def product(request, product_id='all'):
    if request.method == 'GET':
        if product_id == 'all':
            return unicode_response(query_api(request, Registration.objects.all(), 'products'))
        else:
            print('klein')
            registration = Registration.objects.get(pk=int(product_id))
            return unicode_response(registration.serialize())
    elif request.method in ['POST', 'PUT']:
        if product_id == 'all':
            return unicode_response({'message' : 'Invalid Request'}, status=400)
        elif not authenticate_token(request):
            return unicode_response({'message' : 'Forbidden'}, status=403)
        else:
            return create_or_update_product(request, int(product_id))
    elif request.method in ['PATCH']:
        if product_id == 'all':
            return unicode_response({'message' : 'Invalid Request'}, status=400)
        elif not authenticate_token(request):
            return unicode_response({'message' : 'Forbidden'}, status=403)
        else:
            return patch_product(request, int(product_id))
    elif request.method == 'DELETE':
        print(request.META)
        if product_id == 'all':
            return unicode_response({'message' : 'Invalid Request'}, status=400)
        elif not authenticate_token(request):
            return unicode_response({'message' : 'Forbidden'}, status=403)
        else:
            return remove_product(request, int(product_id))


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def price(request):
    if request.method == 'POST':
        if not authenticate_token(request):
            return unicode_response({'message' : 'Forbidden'}, status=403)
        else:
            return create_price(request)
    elif request.method == 'GET':
        return query_prices(request)
