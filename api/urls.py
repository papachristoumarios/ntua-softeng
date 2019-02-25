from django.conf.urls import url
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    url(r'login', obtain_auth_token, name='login'),
    url(r'logout', views.logout_user, name='logout'),
    url(r'prices', views.price, name='prices'),
    url(r'products', include([
        url(r'(?P<product_id>\w+)', views.product),
        url(r'', views.product),
    ])),
    url(r'shops', include([
        url(r'(?P<shop_id>\w+)', views.shop),
        url(r'', views.shop),
    ])),
]
