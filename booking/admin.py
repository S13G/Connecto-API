from decimal import Decimal
from django.contrib import admin

from booking.models import Place, Booking, EquipmentChoice, Vehicle, EquipmentType, Country

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

@admin.register(EquipmentChoice)
class EquipmentChoiceAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'quantity', 'total_price']


class BookingAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'from_place', 'to_place', 'total_current_price']
    readonly_fields = ['transaction_id', 'stripe_token']
    list_filter = ('first_name', 'last_name', 'transaction_id', 'stripe_token')

    fieldsets = (
        ('Booker', {'fields': ['pronoun', 'first_name', 'last_name', 'email_address', 'phone_number', 'country']}),
        ('Journey Details', {'fields': ['from_place', 'to_place', 'vehicle', 'passengers', 'equipment_choices']}),
        ('Other Details', {'fields': ['route', 'departure', 'returning', 'arrival_flight_number', 'departure_flight_number', 'drop_off', 'pickup_address']}),
        ('Dates and Timings', {'fields': ['landing_time', 'return_date', 'pickup_time', 'departure_flight_time', 'date_filled']}),
        ('Payment Details', {'fields': ['transaction_id', 'verified', 'stripe_token']}),

    )

    @admin.display(description='Full name')
    def full_name(self, obj):
        return f"{obj.pronoun} {obj.first_name} {obj.last_name}"
    
    def has_add_permission(self, request):
        return False

admin.site.register(EquipmentType)
admin.site.register(Booking, BookingAdmin)
