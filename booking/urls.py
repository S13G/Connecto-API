from django.urls import path
from booking.views import BookVehicleView, BookingUpdateView, CountryView, EquipmentTypeView, PlaceView, VehicleView

urlpatterns = [
    path('places/', PlaceView.as_view()),
    path('countries/', CountryView.as_view()),
    path('vehicles/', VehicleView.as_view()),
    path('equipment-types/', EquipmentTypeView.as_view()),
    path('book-vehicle/', BookVehicleView.as_view()),
    path('check-update-booking/<slug:sess_key>/', BookingUpdateView.as_view()),
]