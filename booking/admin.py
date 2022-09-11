from django.contrib import admin
# from django.contrib.gis.admin import OSMGeoAdmin

from booking.models import Place, Booker, Booking, Journey, EquipmentChoice, Vehicle, EquipmentType, Country

# Register your models here.


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'category', 'code']
    list_per_page = 30
    list_select_related = ['country']
    ordering = ['name']
    readonly_fields = ['longitude', 'latitude']
    search_fields = ['name', 'code']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    list_per_page = 30
    ordering = ['name']
    search_fields = ['name', 'code']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_make_and_model', 'category', 'current_price', 'old_price']
    list_editable = ['current_price', 'old_price']
    list_per_page = 30
    ordering = ['vehicle_make_and_model']


@admin.register(Booker)
class BookerAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    list_per_page = 30
    list_select_related = ['country']
    ordering = ['first_name']

    @admin.display(description='Full name')
    def name(self, obj):
        return ("%s %s %s" % (obj.pronoun, obj.first_name, obj.last_name))


@admin.register(EquipmentChoice)
class EquipmentChoiceAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'quantity', 'price']
    readonly_fields = ['price']


class BookingInline(admin.StackedInline):
    model = Booking
    max_num = 1


@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    inlines = [BookingInline,]
    list_display = ['from_place', 'to_place', 'distance', 'current_price', 'with_return_current_price']
    list_per_page = 30
    readonly_fields = ['old_price', 'current_price', 'distance']


admin.site.register([Booking, EquipmentType])