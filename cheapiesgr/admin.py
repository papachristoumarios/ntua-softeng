from django.contrib.gis import admin
from .models import *
from django.contrib.gis.db import models as gis_models

class PointAdmin(admin.OSMGeoAdmin):	#Class using OSMGeoadmin
    default_lon = 2642481.7 #lon of Athens
    default_lat = 4576976.96 #lat of Athens
    map_width = 600  # Dimensions of the
    map_height = 400 # map (pixels)
    default_zoom = 11 #Appropriate zoom

admin.site.register([Shop, Volunteer, Registration,Category],PointAdmin)
