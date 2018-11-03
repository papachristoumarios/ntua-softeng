from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'map', views.default_map, name='map'),
    url(r'signup', views.signup, name='signup'),
    url(r'signin', views.signin, name='signin'),
    url(r'product', views.product, name='product'),
    url(r'privacy', views.privacy, name='privacy'),
    url(r'', views.index, name='index'),
]
