from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from booking.models import Booking, Country, EquipmentType, Place, PlaceReview, Vehicle, VehicleReview
from booking.serializers import BookVehicleSerializer


class PlaceView(APIView):
    @swagger_auto_schema(
        operation_summary="List of all places(City, Airports etc.)"
    )
    def get(self, request):
        places = Place.objects.select_related('country')
        data = []
        for p in places:
            reviews = p.place_reviews.all()
            count = reviews.count()
            ratings = 0
            if count > 1:
                ratings = (sum([r.percentage for r in reviews])) / count
            data.append({'name': p.name, 'country': p.country.name, 'category': p.category, 'code': p.code,
                         'longitude': p.longitude, 'latitude': p.latitude, "ratings": ratings}.copy())
        return Response(data, status=200)


class CountryView(APIView):
    @swagger_auto_schema(
        operation_summary="List of all countries"
    )
    def get(self, request):
        countries = Country.objects.values('name', 'code')
        return Response(countries, status=200)


class VehicleView(APIView):
    @swagger_auto_schema(
        operation_summary="List of all vehicles with additional info e.g price etc."
    )
    def get(self, request):
        vehicles = Vehicle.objects.all()
        data = []
        for v in vehicles:
            reviews = v.vehicle_reviews.all()
            count = reviews.count()
            ratings = 0
            if count > 1:
                ratings = (sum([r.percentage for r in reviews])) / count
            data.append({'vehicle_make_and_model': v.vehicle_make_and_model, 'category': v.category, 'seats': v.seats,
                         'baggage': v.baggage, 'tag': v.tag, 'current_price': v.current_price, "old_price": v.old_price,
                         "ratings": ratings}.copy())
        return Response(data, status=200)


class EquipmentTypeView(APIView):
    @swagger_auto_schema(
        operation_summary="List of equipment types to be selected from(will be chosen in the equipment choice section)"
    )
    def get(self, request):
        types = EquipmentType.objects.values('name', 'price')
        return Response(types, status=200)


class BookVehicleView(CreateAPIView):
    serializer_class = BookVehicleSerializer
    queryset = Booking.objects.all()


class PlaceReviewView(APIView):
    @swagger_auto_schema(
        operation_summary="Adding a review to a place service"
    )
    def post(self, request):
        data = request.data
        original_keys = ['place_name', 'name', 'email', 'message', 'percentage']
        if set(original_keys) == set(data.keys()) and not None in data.values() and not "" in data.values():
            email = data.get('email')
            try:
                validate_email(email)
            except ValidationError as e:
                return Response('Invalid Email', status=400)

            if not isinstance(data.get('percentage'), int):
                return Response("Percentage must be an integer", status=400)

            place = Place.objects.filter(name=data.get("place_name"))
            if not place.exists():
                return Response("Place with that name does not exist", status=400)

            PlaceReview.objects.create(place=place, name=data.get('name'), email=email, message=data.get('message'),
                                       percentage=data.get('percentage'))
            return Response("Review sent", status=200)
        else:
            return Response("You didn't enter all required fields correctly", status=400)


class VehicleReviewView(APIView):
    @swagger_auto_schema(
        operation_summary="Adding a review to a vehicle(also using star ratings)"
    )
    def post(self, request):
        data = request.data
        original_keys = ['vehicle_make_and_model', 'name', 'email', 'message', 'percentage']
        if set(original_keys) == set(data.keys()) and not None in data.values() and not "" in data.values():
            email = data.get('email')
            try:
                validate_email(email)
            except ValidationError as e:
                return Response('Invalid Email', status=400)

            if not isinstance(data.get('percentage'), int):
                return Response("Percentage must be an integer", status=400)

            vehicle = Vehicle.objects.filter(vehicle_make_and_model=data.get("vehicle_make_and_model"))
            if not vehicle.exists():
                return Response("Vehicle with that make does not exist", status=400)

            VehicleReview.objects.create(vehicle_make_and_model=data.get("vehicle_make_and_model"),
                                         name=data.get('name'), email=email, message=data.get('message'),
                                         percentage=data.get('percentage'))
            return Response("Review sent", status=200)
        else:
            return Response("You didn't enter all required fields correctly", status=400)

# {
#    "stripe_token": "GENERATED_STRIPE_TOKEN"
# }
