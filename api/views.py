import datetime
import json
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
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

def parse_withdrawn(data):
	if data['withdrawn'] in [True, 'true']:
		return True
	else:
		return False

def unicode_response(data, status=200):
	""" Returns unicode response """
	if status == 200:
		return HttpResponse(
			json.dumps(
				data,
				indent=4,
				sort_keys=True,
				ensure_ascii=False),
			content_type="application/json",
			status=status)
	else:
		return HttpResponse(
			json.dumps(
				data,
				indent=4,
				ensure_ascii=False),
			status=status)


def build_list_from_queryset(query_set):
	""" Returns a list of serialized objects """
	result = []
	for x in query_set:
		result.append(x.serialize())
	return result


def build_list_from_price_queryset(query_set, location_point):
	""" Returns a list of serialized RegistrationPrice objects """
	result = []
	for x in query_set:
		result.append(x.serialize(location_point))

	return result


def authenticate_token(request):
	""" Authenicate a user via token """
	try:
		user = Token.objects.get(key=request.META[AUTH_TOKEN_LABEL]).user
		return True
	except BaseException:
		return False


def is_superuser(request):
	""" Returns true if user is superuser """
	user = Token.objects.get(key=request.META[AUTH_TOKEN_LABEL]).user
	return user.is_superuser


def get_request_data(request):
	""" Returns request data from body """
	temp = dict(QueryDict(request.body))
	data = dict([(key, val[0]) for key, val in temp.items()])
	return data


def query_shops_and_products(request, objects, list_label):
	""" Implements GET /products and GET /prices """
	# Get arguments
	start = int(request.GET.get('start', 0))
	count = int(request.GET.get('count', 20))
	status = request.GET.get('status', 'ACTIVE')
	sort = request.GET.get('sort', 'id|DESC')
	total = objects.count()

	if start < 0:
		return unicode_response({'message': 'Invalid start'}, status=400)

	if count <= 0:
		return unicode_response({'message': 'Invalid count'}, status=400)

	# Status
	if status == 'ACTIVE':
		status_result = objects.filter(withdrawn=False)
	elif status == 'WITHDRAWN':
		status_result = objects.filter(withdrawn=True)
	elif status == 'ALL':
		status_result = objects
	else:
		return unicode_response({'message': 'Invalid status'}, status=400)

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
		return unicode_response(
			{'message': 'Invalid sort criterion'}, status=400)

	# Paginate
	try:
		paginator = Paginator(sort_result, count)
		result = paginator.page(start + 1)
	except BaseException:
		return unicode_response({'message': 'Invalid pagination'}, status=400)

	data = {
		'start': start,
		'count': count,
		'total': total,
		list_label: build_list_from_queryset(result)
	}
	return data


def create_or_update_shop(request, shop_id):
	""" Implements POST /shops/<id> and PUT /shops/<id> """
	try:
		data = get_request_data(request)
		if request.method == 'POST':
			shop = Shop(
				name=data['name'],
				address=data['address'],
				city=data['address'],
				withdrawn=parse_withdrawn(data),
				location='SRID=4326;POINT({} {})'.format(data['lng'],data['lat']),
				tags=json.dumps(data['tags'], ensure_ascii=False)
			)
			shop.save()
		elif request.method == 'PUT':
			shop = Shop.objects.get(pk=int(shop_id))
			shop.name = data['name']
			shop.address = data['address']
			shop.city = data['address']
			shop.tags = json.dumps(data['tags'], ensure_ascii=False)
			shop.withdrawn = data['withdrawn']
			lat = data.get('lat', shop.location.y)
			lon = data.get('lng', shop.location.x)
			shop.location = 'SRID=4326;POINT({} {})'.format(lon, lat)
			shop.save()
		return unicode_response(
			{'message': 'Shop created sucessfully'}, status=200)
	except BaseException:
		return unicode_response(
			{'message': 'Parameters not valid'}, status=400)


def patch_shop(request, shop_id):
	""" Implements PATCH /shops/<id> """
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
			lat = data.get('lat', shop.location.y)
			lon = data.get('lng', shop.location.x)
			shop.location = 'SRID=4326;POINT({} {})'.format(lon, lat)
		shop.save()
		return unicode_response(
			{'message': 'Shop patched sucessfully'}, status=200)
	except BaseException:
		return unicode_response(
			{'message': 'Parameters not valid'}, status=400)


def remove_shop(request, shop_id):
	""" Implements DELETE /shops/<id> """
	try:
		shop = Shop.objects.get(id=shop_id)
		if is_superuser(request):
			shop.delete()
			return unicode_response({'message': 'Removal successfull'})
		else:
			shop.withdrawn = True
			shop.save()
			return unicode_response({'message': 'Withdrawal successfull'})

	except BaseException:
		return unicode_response(
			{'message': 'Parameters not valid'}, status=400)


def parse_date(date_str):
	""" Parse a date """
	if date_str == '-1':
		return -1
	else:
		format_str = '%Y-%m-%d'
		return datetime.datetime.strptime(date_str, format_str)


def create_price(request):
	""" Implement POST /price """
	price = RegistrationPrice(
		date_from=parse_date(request.POST['dateFrom']),
		date_to=parse_date(request.POST['dateTo']),
		price=request.POST['price'],
		shop_id=int(request.POST['shopId']),
		registration_id=int(request.POST['productId'])
	)
	price.save()
	return unicode_response({'message': 'Price creation sucessfull'})


def parse_location(request):
	""" Parse location for geodesic query """
	if 'geoDist' in request.GET and 'geoLng' in request.GET and 'geoLat' in request.GET:
		assert(float(request.GET['geoDist']) >= 0)
		return Point(
			float(
				request.GET['geoLng']), float(
				request.GET['geoLat']), srid=4326), float(
			request.GET['geoDist'])
	elif 'geoDist' not in request.GET and 'geoLng' not in request.GET and 'geoLat' not in request.GET:
		return None, -1
	else:
		return None, None


def list_to_regex(l):
	return r'|'.join(l)


def query_prices(request):
	""" Implements GET /prices """
	# Query parameters
	start = request.GET.get('start', 0)
	count = request.GET.get('count', 20)
	date_from = parse_date(request.GET.get('dateFrom', '1969-01-01'))
	date_to = parse_date(request.GET.get('dateTo', '2300-01-01'))
	sort = request.GET.get('sort', 'price|ASC')
	shops = [int(x) for x in request.GET.getlist('shops', [])]
	products = [int(x) for x in request.GET.getlist('products', [])]
	tags = list_to_regex(request.GET.getlist('tags', []))
	location_point, dist = parse_location(request)
	print(products)

	# Check parameters
	if start < 0:
		return unicode_response({'message': 'Invalid start'}, status=400)

	if count <= 0:
		return unicode_response({'message': 'Invalid count'}, status=400)

	if date_from > date_to:
		return unicode_response({'message': 'Invalid dates'}, status=400)

	if location_point is None and dist is None:
		return unicode_response({'message': 'Invalid location'}, status=400)

	prices = RegistrationPrice.objects

	# Filter date
	date_filtered = prices.filter(
		date_from__gte=date_from,
		date_to__lte=date_to)

	# Filter distance
	if location_point is not None and dist is not None:
		degrees = dist * 1 / 111.325
		distance_filtered = date_filtered.filter(
			shop__location__distance_lte=(
				location_point, degrees))

	# Filter products
	products_filtered = date_filtered.filter(registration_id__in=products)

	# Filter shops
	shops_filtered = products_filtered.filter(shop_id__in=shops)

	# Filter tags
	tags_filtered = products_filtered.filter(
		registration__tags__iregex=tags) | products_filtered.filter(
		shop__tags__iregex=tags)

	# Sorting
	if sort == 'price|ASC':
		sort_result = tags_filtered.order_by('price')
	elif sort == 'price|DESC':
		sort_result = tags_filtered.order_by('-price')
	elif sort == 'date|ASC':
		sort_result = tags_filtered.order_by('date_from')
	elif sort == 'date|DESC':
		sort_result = tags_filtered.order_by('-date_from')
	elif sort == 'geo.dist|ASC':
		sort_result = tags_filtered.annotate(distance=Distance(
			"shop__location", location_point)).order_by('distance')
	elif sort == 'geo.dist|DESC':
		sort_result = tags_filtered.annotate(
			distance=Distance(
				"shop__location",
				location_point)).order_by('-distance')

	# Paginate
	try:
		paginator = Paginator(sort_result, count)
		result = paginator.page(start + 1)
	except BaseException:
		return unicode_response({'message': 'Invalid pagination'}, status=400)

	# Response
	data = {
		'start': start,
		'count': count,
		'total': sort_result.count(),
		'prices': build_list_from_price_queryset(result, location_point)

	}
	return unicode_response(data)


def create_or_update_product(request, product_id):
	""" Implements POST /products/<id> and PUT /products/<id> """
	# try:
	user = Token.objects.get(key=request.META[AUTH_TOKEN_LABEL]).user
	data = get_request_data(request)
	print(request.body.decode('iso-8859-1'))
	print(data)
	if request.method == 'POST':
		# TODO Remove price and shop
		try:
			category = Category.objects.get(category_name=data['category'])
		except:
			category = Category(category_name=data['category'])
			category.save()
		registration = Registration(
			name=data['name'],
			product_description=data['description'],
			category=category,
			tags=json.dumps(data['tags'], ensure_ascii=False),
			withdrawn=parse_withdrawn(data),
			price=0,
			volunteer=user,
		)
		registration.save()
		return unicode_response(
			{'message': 'Product created sucessfully'}, status=200)
	elif request.method == 'PUT':
		registration = Registration.objects.get(pk=int(product_id))
		registration.name = data['name']
		registration.product_description = data['description']
		registration.tags = json.dumps(data['tags'], ensure_ascii=False)
		registration.withdrawn = data['withdrawn']
		registration.volunteer = user
		try:
			category = Category.objects.get(category_name=data['category'])
		except:
			category = Category(category_name=data['category'])
			category.save()
		registration.category = category
		registration.save()
		return unicode_response(
			{'message': 'Product put sucessfully'}, status=200)
# except BaseException:
	# 	return unicode_response(
	# 		{'message': 'Parameters not valid'}, status=400)


def remove_product(request, product_id):
	""" Implements DELETE /products/<id> """
	try:
		registration = Registration.objects.get(id=product_id)
		if is_superuser(request):
			registration.delete()
			return unicode_response({'message': 'Removal successfull'})
		else:
			registration.withdrawn = True
			registration.save()
			return unicode_response({'message': 'Withdrawal successfull'})
	except BaseException:
		return unicode_response(
			{'message': 'Parameters not valid'}, status=400)


def patch_product(request, product_id):
	""" Implements PATCH /products/<id> """
	try:
		registration = Registration.objects.get(pk=product_id)
		data = get_request_data(request)
		if 'name' in data:
			registration.name = data['name']
		if 'description' in data:
			registration.product_description = data['description']
		if 'category' in data:
			category = Category.objects.get(category_name=data['category'])
			registration.category = category
		if 'tags' in data:
			registration.tags = json.dumps(data['tags'], ensure_ascii=False)
		if 'withdrawn' in data:
			registration.withdrawn = data['withdrawn']
		registration.save()
		return unicode_response(
			{'message': 'Product patched sucessfully'}, status=200)
	except BaseException:
		return unicode_response(
			{'message': 'Parameters not valid'}, status=400)


# TODO Implement
@csrf_exempt
@require_http_methods(['POST'])
def create_user(request):
	return None


@csrf_exempt
@require_http_methods(['POST'])
def logout_user(request):
	""" Implements POST /logout """
	token = request.META[AUTH_TOKEN_LABEL]
	try:
		user = Token.objects.get(key=token).user
		user.auth_token.delete()
		return unicode_response({'message': 'OK'})
	except BaseException:
		return unicode_response(
			{'message': 'Token not associated with user'}, status=400)


@csrf_exempt
@require_http_methods(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def shop(request, shop_id='all'):
	""" Endpoint handler for /shops """
	if request.method == 'GET':
		if shop_id == 'all':
			return unicode_response(
				query_shops_and_products(
					request, Shop.objects.all(), 'shops'))
		else:
			shop = Shop.objects.get(pk=int(shop_id))
			return unicode_response(shop.serialize())
	elif request.method in ['POST', 'PUT']:
		if not authenticate_token(request):
			return unicode_response({'message': 'Forbidden'}, status=403)
		else:
			return create_or_update_shop(request, shop_id)
	elif request.method == 'PATCH':
		if shop_id == 'all':
			return unicode_response({'message': 'Invalid Request'}, status=400)
		elif not authenticate_token(request):
			return unicode_response({'message': 'Forbidden'}, status=403)
		else:
			return patch_shop(request, int(shop_id))
	elif request.method == 'DELETE':
		if shop_id == 'all':
			return unicode_response({'message': 'Invalid Request'}, status=400)
		elif not authenticate_token(request):
			return unicode_response({'message': 'Forbidden'}, status=403)
		else:
			return remove_shop(request, int(shop_id))


@csrf_exempt
@require_http_methods(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def product(request, product_id='all'):
	""" Endpoint handler for /products """
	if request.method == 'GET':
		if product_id == 'all':
			return unicode_response(
				query_shops_and_products(
					request,
					Registration.objects.all(),
					'products'))
		else:
			registration = Registration.objects.get(pk=int(product_id))
			return unicode_response(registration.serialize())
	elif request.method in ['POST', 'PUT']:
		if not authenticate_token(request):
			return unicode_response({'message': 'Forbidden'}, status=403)
		else:
			return create_or_update_product(request, product_id)
	elif request.method in ['PATCH']:
		if product_id == 'all':
			return unicode_response({'message': 'Invalid Request'}, status=400)
		elif not authenticate_token(request):
			return unicode_response({'message': 'Forbidden'}, status=403)
		else:
			return patch_product(request, int(product_id))
	elif request.method == 'DELETE':
		print(request.META)
		if product_id == 'all':
			return unicode_response({'message': 'Invalid Request'}, status=400)
		elif not authenticate_token(request):
			return unicode_response({'message': 'Forbidden'}, status=403)
		else:
			return remove_product(request, int(product_id))


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def price(request):
	""" Endpoint handler for /prices """
	if request.method == 'POST':
		if not authenticate_token(request):
			return unicode_response({'message': 'Forbidden'}, status=403)
		else:
			return create_price(request)
	elif request.method == 'GET':
		return query_prices(request)
