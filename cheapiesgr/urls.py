from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'map', views.default_map, name="map"),
    url(r'signup', views.signup, name="signup"),
    url(r'', views.index, name="index"),
]
