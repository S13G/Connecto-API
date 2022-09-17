from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from booking.models import Booking, Country, EquipmentType, Place, Vehicle
from booking.serializers import BookVehicleSerializer

class PlaceView(APIView):
   def get(self, request):
      places = Place.objects.select_related('country')
      data = []
      for p in places:
         data.append({'name': p.name, 'country':p.country.name, 'category':p.category, 'code':p.code, 'longitude':p.longitude, 'latitude':p.latitude}.copy())
      return Response(data, status=200)

class CountryView(APIView):
   def get(self, request):
      countries = Country.objects.values('name', 'code')
      return Response(countries, status=200)

class VehicleView(APIView):
   def get(self, request):
      vehicles = Vehicle.objects.values('vehicle_make_and_model', 'category', 'seats', 'baggage', 'tag', 'current_price', 'old_price')
      return Response(vehicles, status=200)

class EquipmentTypeView(APIView):
   def get(self, request):
      types = EquipmentType.objects.values('name', 'price')
      return Response(types, status=200)

class BookVehicleView(CreateAPIView):
   serializer_class = BookVehicleSerializer
   queryset = Booking.objects.all()
