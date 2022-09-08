from django.contrib import admin
# from django.contrib.gis.admin import OSMGeoAdmin

from booking.models import Place, Booker, Booking, Journey, Equipment, Vehicle, EquipmentType, Country

# Register your models here.


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


# @admin.register(GeoFence)
# class GeoFenceAdmin(OSMGeoAdmin):
#     list_display = ['name', 'geofence']


admin.site.register([Journey, Vehicle, Booker,
                    Booking, Equipment, EquipmentType, Country])
