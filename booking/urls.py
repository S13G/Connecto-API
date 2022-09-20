from django.urls import path
from booking.views import BookVehicleView, CountryView, EquipmentTypeView, PlaceView, VehicleView

urlpatterns = [
    path('places/', PlaceView.as_view()),
    path('countries/', CountryView.as_view()),
    path('vehicles/', VehicleView.as_view()),
    path('equipment-types/', EquipmentTypeView.as_view()),
    path('book-vehicle/', BookVehicleView.as_view()),
]

