from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    url(r'login', obtain_auth_token, name='login'),
    url(r'logout', views.logout_user, name='logout'),
    url(r'products', views.product, name='products'),
    url(r'shops', views.shop, name='shops'),
    url(r'prices', views.price, name='prices'),
]
