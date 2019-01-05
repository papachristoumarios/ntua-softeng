from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'addproduct', views.addproduct, name='addproduct'),
    url(r'answer', views.answer, name='answer'),
    url(r'map', views.default_map, name='map'),
    url(r'logout', views.signout, name='logout'),
    url(r'signup', views.signup, name='signup'),
    url(r'signin', views.signin, name='signin'),
    url(r'product', views.product, name='product'),
    url(r'privacy', views.privacy, name='privacy'),
    url(r'profile', views.profile, name='profile'),
    url(r'search', views.search, name='search'),
    url(r'removeFavorite', views.remove_favorite, name='removeFavorite'),
    url(r'report', views.report, name='report'),
    url(r'userauthentication', views.user_auth, name='userauthentication'),
    url(r'', views.index, name='index'),
]
