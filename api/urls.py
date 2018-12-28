from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    url(r'login', obtain_auth_token, name='login'),
    url(r'logout', views.logout, name='logout'),
    url(r'products', views.get_products, name='products'),
    url(r'shops', views.get_shops, name='shops'),
    url(r'prices', views.get_prices, name='prices'),
]
