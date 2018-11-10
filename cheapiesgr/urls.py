from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'newproduct1', views.newproduct1, name='newproduct1'),
    url(r'newproduct2', views.newproduct2, name='newproduct2'),
    url(r'newproduct3', views.newproduct3, name='newproduct3'),
    url(r'addproduct', views.addproduct, name='addproduct'),
    url(r'map', views.default_map, name='map'),
    url(r'signup', views.signup, name='signup'),
    url(r'signin', views.signin, name='signin'),
    url(r'product', views.product, name='product'),
    url(r'privacy', views.privacy, name='privacy'),
    url(r'profile', views.profile, name='profile'),
    url(r'search', views.search, name='search'),
    url(r'', views.index, name='index'),
]
